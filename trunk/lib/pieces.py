#!/usr/bin/env python
# -*-coding: utf-8 -*-
# Filename: pieces.py

import pygame
from pygame.locals import RLEACCEL
import os
import glob
import math
import random
from pprint import pprint

import utils
import data
from config import *
import music

from levelposimages import level_pos
from explosion import *



DEBUG_MANUEL = True
class EnergyBar(pygame.sprite.Sprite):
    '''An energy bar'''
    def __init__(self, energy_leap=0.05):
        pygame.sprite.Sprite.__init__(self)
        self.energy_leap = energy_leap
        self.energy_percent = 100 #percent remanding of time
        self.image = self._image()
        self.rect = self.image.get_rect(right=WIDTH-10, bottom=HEIGHT)

    def update(self):
        self.energy_percent -= self.energy_leap
        self.image = self._image()
        self.rect = self.image.get_rect(right=WIDTH-10, bottom=HEIGHT)

    def add_energy(self, add_percent):
        self.energy_percent = min(100, add_percent + self.energy_percent)
        
    def _image(self):
        #font = pygame.font.Font(FONT1, 14)
        #text = font.render("Energy", True, BLACK)
        w = 15
        h = max(int(WIDTH * self.energy_percent / 100), 0)

        if self.energy_percent > 60: 
            color = GREEN
        elif self.energy_percent > 30:
            color = ORANGE
        else:
            color = RED
        img = utils.create_surface((w,h), color)
        #w1 = img.get_rect().width
        #w2 = text.get_rect().width
        #if w1 > 1.2 * w2:        
            #img.blit(text, (w1 - w2, 0))
        return img


class StaticPiece(pygame.sprite.Sprite):
    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id

        self.set_position()

    def set_position(self):
        t,l = level_pos[self.level][self.id]
        self.rect.topleft = t + ROBOT_OFFSET[0], l + ROBOT_OFFSET[1]
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.image.set_alpha(50)

    def __str__(self):
        return "Pieza %d" % (self.id,)

class FacePiece(StaticPiece):

    def set_position(self):
        t,l = level_pos[self.level][2]  #2 es la cara en todos los niveles
        self.rect.topleft = t + ROBOT_OFFSET[0] + 15, l + ROBOT_OFFSET[1] + 10

class DinamicPiece(pygame.sprite.Sprite):
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2),
                 lambda x: x]

    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id
        self.selected = False
        self.selected_time = 0
        self.desfasaje_rotacion = 0

        self.set_top_position()

    def set_top_position(self):
        self.num = self.count()
        self.func_x = random.choice(self.functions)
        angle = random.choice([90, 180, 270])
        self.rotate(angle)
        self.rect.bottom = 0
        # define el rango de cordenadas en las que pueden aparecer las
        # piezas (cordenada y solamente, x aparecen en 0)
        cordenates = range(WIDTH) # alto
        self.x = random.choice(cordenates)
        self.y = 0

    def _velocity(self):
        #largo, ancho = self.rect.size
        #vel = (largo * ancho) / float(500) + 2
        ##print "Velocidad: ",vel
        #return min(30, vel)
        return 16

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect()
        self.desfasaje_rotacion = (self.desfasaje_rotacion + angle) % 360

    def update(self):
        if self.rect.top > HEIGHT:
            return

        if self.selected:
            self.rect.center   = pygame.mouse.get_pos()
            self.selected_time -= 1
            if self.selected_time == 0:
                self.dispatcher.selected_explosion()
        else:
            num = self.num.next()
            num = math.radians(num)
            func_y = 10*num

            pos = (self.func_x(num) + self.x, func_y + self.y)
            self.rect.center = pos
            if self.rect.top > HEIGHT:
                self.rect.move_ip(0, pos[1])
                self.num = self.count()
                self.y = 0

    def count(self, x=0):
        i = self._velocity()
        x = x
        while 1:
            x = x+i
            yield x


class WrongPiece(DinamicPiece):

    def __init__(self, id, img, level):
        DinamicPiece.__init__(self, id, img, level)

    def update(self):
        if self.rect.top > HEIGHT:
            return

        num = self.num.next()
        num = math.radians(num)
        func_y = 10*num

        pos = (self.func_x(num) + self.x, func_y + self.y)
        self.rect.center = pos
        if self.rect.top > HEIGHT:
            self.rect.move_ip(0, pos[1])
            self.num = self.count()
            self.y = 0

    def is_erronea(self):
        return True

class RightPiece(DinamicPiece):

    def __init__(self, id, img, level):
        DinamicPiece.__init__(self, id, img, level)

    def release(self):
        music.stop_peep()
        self.selected = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.num = self.count()
        self.x = mouse_x
        self.y = mouse_y

    def select(self, miliseconds=2000):
        music.play_peep()
        self.selected = True
        self.selected_time = (miliseconds * CLOCK_TICS) / 1000

    def fit(self, robot):
        #print self.desfasaje_rotacion
        if self.desfasaje_rotacion:
            return False

        collideds = pygame.sprite.spritecollide(self, robot, False)
        
        target = [x for x in collideds if x.id == self.id ]

        if target:
            self.rect.topleft = target[0].rect.topleft
            return True
        return False

    def update(self):
        if self.rect.top > HEIGHT:
            return

        if self.selected:
            self.rect.center   = pygame.mouse.get_pos()
            self.selected_time -= 1
            if self.selected_time == 0:
                self.dispatcher.selected_explosion()
        else:
            num = self.num.next()
            num = math.radians(num)
            func_y = 10*num

            pos = (self.func_x(num) + self.x, func_y + self.y)
            self.rect.center = pos
            if self.rect.top > HEIGHT:
                self.rect.move_ip(0, pos[1])
                self.num = self.count()
                self.y = 0

    def is_erronea(self):
        return False

class Pieces(object):
    def __init__(self, level, type_piece="static"):
        self.level = level
        self.type_piece = type_piece
        self.images = self.load_images()

    def load_images(self):
        if self.type_piece in ("static", "dinamic"): 
            result = []
            for pathfile in glob.glob(os.path.join(PIECES_LEVEL[self.level], '*.png')):
                myFile = os.path.basename(pathfile)
                myId = myFile[:-4]
                image = utils.load_image_alpha(pathfile, -1)
                result.append((int(myId), image))
        elif self.type_piece == "erronea":
            result = []
            for pathfile in glob.glob(os.path.join(ERRONEAS_LEVEL[self.level], '*.png')):
                myFile = os.path.basename(pathfile)
                myId = myFile[:-4]
                image = utils.load_image_alpha(pathfile, -1)
                result.append((int(myId), image))
        elif self.type_piece == "face":
            result = []
            for pathfile in glob.glob(os.path.join(FACES, '*.png')):
                myFile = os.path.basename(pathfile)
                myId = myFile[:-4]
                image = utils.load_image_alpha(pathfile, -1)
                result.append((int(myId), image))
        return result

    def get_all(self):
        result = []
        for img in self.images:
            if self.type_piece == "static":
                piece = StaticPiece(img[0], img[1], self.level)
            elif self.type_piece == "dinamic":
                piece = RightPiece(img[0], img[1], self.level)
            elif self.type_piece == "erronea":
                piece = WrongPiece(img[0], img[1], self.level)
            elif self.type_piece == "face":
                piece = FacePiece(img[0], img[1], self.level)
            result.append(piece)
        return result

class Dispatcher(object):
    def __init__(self, mount, piezas_activas, piezas, piezas_erroneas, piezas_encajadas, robot):
        #mount es la cantidad de piezas que son despachadas de forma simultanea
        self.mount = mount
        self.piezas_activas   = piezas_activas
        self.piezas           = piezas
        self.piezas_erroneas  = piezas_erroneas
        self.piezas_encajadas = piezas_encajadas
        self.robot = robot

        for p in self.piezas:
            p.dispatcher = self

        self.mouse_with_piece = False
        self.mouse_with_erronea_piece = False

    def selected_explosion(self):
        music.stop_peep()
        self.selected_piece.selected = False
        self.mouse_with_piece = False
        self.piezas_activas.remove(self.selected_piece)
        ExplosionMedium(self.selected_piece.rect.center)
        self.selected_piece.set_top_position()

    def new_dispatch(self):
        if self.mouse_with_erronea_piece:
            return True

        if not self.piezas_activas.sprites():
            return True

        for p in self.piezas_activas:
            if p.rect.top < HEIGHT:
                return False
        return True

    def dispatch(self):
        if not self.new_dispatch():
            return

        self.piezas_activas.empty()
        self.mouse_with_erronea_piece = False

        #Agrego las piezas erroneas
        erroneas_options = self.piezas_erroneas.sprites()
        for i in range(self.mount):
            pieza = random.choice(erroneas_options)
            erroneas_options.remove(pieza)
            pieza.set_top_position()
            self.piezas_activas.add(pieza)

        #Agrego la pieza correcta
        if self.piezas.sprites():
            pieza          = random.choice(self.piezas.sprites())
            pieza.set_top_position()
            self.piezas_activas.add(pieza)

    def rotate_selected(self, angle):
        if self.mouse_with_piece:
            self.selected_piece.rotate(angle)

    def agarrar_soltar(self, pos):
        '''Logica para agarrar o soltar las piezas con el mouse'''
        quepaso = ""
        alguna = False
        for piece in self.piezas_activas:
            if piece.rect.collidepoint(pos):
                self.selected_piece = piece
                alguna = True

                #Primer click (agarrar)
                if not self.mouse_with_piece:
                    if piece.is_erronea():
                        ExplosionMedium(piece.rect.center)
                        self.mouse_with_erronea_piece = True
                        quepaso = "erronea"
                    else:
                        self.mouse_with_piece = True
                        piece.select(miliseconds=2000)
                        #selecciono una pieza correcta
                        quepaso = "correcta"
                #Segundo Click (soltar)
                elif not piece.is_erronea():
                    self.mouse_with_piece = False
                    piece.release()
                    if self.selected_piece.fit(self.robot):
                        self.piezas_encajadas.add(self.selected_piece)
                        self.piezas.remove(self.selected_piece)
                        self.piezas_activas.remove(self.selected_piece)
                        #encajo
                        quepaso = "encajo"
                    #solto afuera
                    else:
                        quepaso = "soltoafuera"
        if not alguna:
            quepaso = "clickafuera"        
        #click afuera
        return quepaso
            

if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces(level=1)
