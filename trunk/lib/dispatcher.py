import pygame
from pygame.locals import RLEACCEL
import random
from pprint import pprint

import utils
from config import *

from levelposimages import *
from explosion import *



class Dispatcher(object):
    def __init__(self, mount, piezas, golden_piezas, piezas_erroneas, \
                piezas_encajadas_atras, piezas_encajadas_adelante, robot, mini_robot, hand):
        #mount es la cantidad de piezas que son despachadas de forma simultanea
        self.mount = mount
        self.piezas           = piezas
        self.golden_piezas     = golden_piezas
        self.piezas_erroneas  = piezas_erroneas
        self.piezas_encajadas_atras = piezas_encajadas_atras
        self.piezas_encajadas_adelante = piezas_encajadas_adelante
        self.robot = robot
        self.mini_robot = mini_robot
        self.hand  = hand
        self.selected_piece = None

        for p in self.piezas.sprites() + self.piezas_erroneas.sprites():
            p.dispatcher = self

    def selected_explosion(self):
        ExplosionMedium(self.selected_piece.rect.center)
        self.selected_piece.release()
        self.selected_piece.set_top_position()
        self.selected_piece = None
        self.hand.release()

    def moving_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_moving()] + \
               [x for x in self.piezas_erroneas.sprites() if x.is_moving()]

    def falling_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_falling()] + \
               [x for x in self.piezas_erroneas.sprites() if x.is_falling()]

    def falling_right_pieces(self):
        return [x for x in self.piezas.sprites() if x.is_falling()]

    def stop_pieces(self):
        return [x for x in self.piezas.sprites() if not x.is_moving()] + \
               [x for x in self.piezas_erroneas.sprites() if not x.is_moving()]
               
    def stop_right_pieces(self):
        return [x for x in self.piezas.sprites() if not x.is_moving()]

    def dispatch(self):
        if random.choice(range(25)):
            return

        if len(self.falling_pieces()) > 8:
            return

        print len(self.golden_piezas)
        if self.stop_pieces():
            if not self.falling_right_pieces() and self.stop_right_pieces():
                piece = random.choice(self.stop_right_pieces())
            else:
                piece = random.choice(self.stop_pieces())
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
            quepaso = self.soltar2()
        else:
            quepaso = self.agarrar()

        if quepaso == "":
            quepaso = "clickafuera"
        #click afuera
        return quepaso

    def soltar2(self):
        self.selected_piece.release()
        self.hand.release()

        if self.selected_piece.fit(self.robot, self.mini_robot):
            if self.selected_piece.prof == ATRAS:
                self.piezas_encajadas_atras.add(self.selected_piece)
            else:   #ADELANTE
                self.piezas_encajadas_adelante.add(self.selected_piece)
            self.piezas.remove(self.selected_piece)
            #encajo
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