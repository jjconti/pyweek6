import pygame
from pygame.locals import RLEACCEL
import random
from pprint import pprint

import utils
from config import *

from levelposimages import *
import music



class Dispatcher(object):
    def __init__(self, mount, piezas, golden_piezas, golden_piezas_used, piezas_erroneas, \
                piezas_encajadas_atras, piezas_encajadas_adelante, robot, mini_robot, hand):
        #mount es la cantidad de piezas que son despachadas de forma simultanea
        self.explosions = 0
        self.mount = mount
        self.piezas           = piezas
        self.golden_piezas     = golden_piezas
        self.golden_piezas_used     = golden_piezas_used
        self.piezas_erroneas  = piezas_erroneas
        self.piezas_encajadas_atras = piezas_encajadas_atras
        self.piezas_encajadas_adelante = piezas_encajadas_adelante
        self.robot = robot
        self.mini_robot = mini_robot
        self.hand  = hand
        self.selected_piece = None
        self.stoped = False

    def explosion(self):
        self.explosions += 1
        self.selected_piece.release()
        self.selected_piece.set_top_position()
        self.selected_piece = None
        self.hand.release()

    def moving_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_moving()] + \
               [x for x in self.piezas_erroneas.sprites() if x.is_moving()] + \
               [x for x in self.golden_pieces.sprites() if x.is_moving()]

    def moving_right_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_moving()]

    def moving_golden_pieces(self):
        return [x for x in self.golden_piezas.sprites() if x.is_moving()]

    def falling_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_falling()] + \
               [x for x in self.piezas_erroneas.sprites() if x.is_falling()] + \
               [x for x in self.golden_piezas.sprites() if x.is_falling()]

    def falling_right_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_falling()]

    def stop_pieces(self):
        return [x for x in self.piezas.sprites() if not x.is_moving()] + \
               [x for x in self.piezas_erroneas.sprites() if not x.is_moving()] + \
               [x for x in self.golden_piezas.sprites() if not x.is_moving()]

    def stop_without_golden_pieces(self):
        return [x for x in self.piezas.sprites() if not x.is_moving()] + \
               [x for x in self.piezas_erroneas.sprites() if not x.is_moving()]

    def stop_golden_pieces(self):
        return [x for x in self.golden_piezas.sprites() if not x.is_moving()]

    def stop_right_pieces(self):
        return [x for x in self.piezas.sprites() if not x.is_moving()]

    def stop(self):
        self.stoped = True

    def dispatch(self):
        if self.stoped or random.choice(range(25)):
            return

        if len(self.falling_pieces()) > 8:
            return

        #print len(self.stop_golden_pieces())

        if self.stop_pieces():
            golden_ids  = [x.id for x in self.moving_golden_pieces()]
            valid_right = [x for x in self.stop_right_pieces() if x.id not in golden_ids]

            right_ids = [x.id for x in self.moving_right_pieces()]
            valid_golden = [x for x in self.stop_golden_pieces() if x.id not in right_ids]

            if not self.falling_right_pieces() and valid_right:
                piece = random.choice(valid_right)
            elif self.moving_golden_pieces():
                piece = random.choice(self.stop_without_golden_pieces())
            else:
                right_ids = [x.id for x in self.moving_right_pieces()]
                piece = random.choice(self.stop_without_golden_pieces() + valid_golden)

            piece.set_top_position()
            piece.move()


    def rotate_selected(self, angle):
        if self.selected_piece:
            self.selected_piece.rotate(angle)

    def agarrar_soltar(self, pos):
        '''Logica para agarrar o soltar las piezas con el mouse'''
        quepaso = ""
        alguna = False
        self.hand.select()

        if self.selected_piece:
            quepaso = self.soltar_selected()
        else:
            quepaso = self.agarrar()

        if quepaso == "":
            quepaso = "clickafuera"
        #click afuera
        return quepaso

    def _remove_fitted_piece(self):
        if self.selected_piece.is_golden():
            self.golden_piezas.remove(self.selected_piece)
            p = [x for x in self.piezas.sprites() if x.id == self.selected_piece.id]
            self.piezas.remove(p)
        else:
            self.piezas.remove(self.selected_piece)
            p = [x for x in self.golden_piezas.sprites() if x.id == self.selected_piece.id]
            self.golden_piezas.remove(p)

    def soltar_selected(self):
        self.selected_piece.release()
        self.hand.release()

        if self.selected_piece.fit(self.robot, self.mini_robot):
            music.play_hammer()
            self._remove_fitted_piece()

            if self.selected_piece.prof == ATRAS:
                self.piezas_encajadas_atras.add(self.selected_piece)
            else:   #ADELANTE
                self.piezas_encajadas_adelante.add(self.selected_piece)
            #self.piezas.remove(self.selected_piece)

            #encajo
            if self.selected_piece.is_golden():
                quepaso = "encajogolden"
            else:
                quepaso = "encajo"
        #solto afuera
        else:
            quepaso = "soltoafuera"

        self.selected_piece = None
        return quepaso

    def soltar(self):
        if not self.selected_piece:
            self.hand.release()

    def agarrar(self):
        quepaso = ""

        for piece in self.falling_pieces():
            if self.hand.collide(piece):
                alguna = True
                if not self.selected_piece:
                    piece.select(miliseconds=2000)
                    #selecciono una pieza
                    if piece.is_wrong():
                        quepaso = "erronea"
                    else:
                        quepaso = "correcta"
                    self.selected_piece = piece
        return quepaso
                    
class DispatcherCredit(Dispatcher):                    
    def __init__(self, piezas, golden_piezas, piezas_erroneas):
        #mount es la cantidad de piezas que son despachadas de forma simultanea
        self.piezas           = piezas
        self.golden_piezas     = golden_piezas
        self.piezas_erroneas  = piezas_erroneas
        self.stoped = False

    def dispatch(self):
        if self.stoped or random.choice(range(25)):
            return

        if len(self.falling_pieces()) > 8:
            return

        #print len(self.stop_golden_pieces())

        if self.stop_pieces():
            golden_ids  = [x.id for x in self.moving_golden_pieces()]
            valid_right = [x for x in self.stop_right_pieces() if x.id not in golden_ids]

            right_ids = [x.id for x in self.moving_right_pieces()]
            valid_golden = [x for x in self.stop_golden_pieces() if x.id not in right_ids]

            if not self.falling_right_pieces() and valid_right:
                piece = random.choice(valid_right)
            elif self.moving_golden_pieces():
                piece = random.choice(self.stop_without_golden_pieces())
            else:
                right_ids = [x.id for x in self.moving_right_pieces()]
                try:
                    piece = random.choice(self.stop_without_golden_pieces() + valid_golden)
                except IndexError:
                    pass
            try:
                       
                piece.set_top_position()
                piece.move()
            except UnboundLocalError:
                pass


