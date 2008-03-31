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

from levelposimages import level_pos
from explosion import *



DEBUG_MANUEL = True

class Piece(pygame.sprite.Sprite):
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2),
                 lambda x: x]

    def __init__(self, id, img, level, static=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id
        self.selected = False
        self.selected_time = 0
        self.desfasaje_rotacion = 0

        self.static = static
        self.set_top_position()

    def set_top_position(self):
        if self.static:
            self.rect.topleft = level_pos[self.level][self.id]
            self.image = self.image.convert()
            self.image.set_colorkey((255,255,255), RLEACCEL)
            self.image.set_alpha(50)
        else:
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
        return 10

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect()
        self.desfasaje_rotacion = (self.desfasaje_rotacion + angle) % 360

    def release(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.num = self.count()
        self.x = mouse_x
        self.y = mouse_y

    def select(self, miliseconds):
        self.selected = True
        self.selected_time = (miliseconds * CLOCK_TICS) / 1000
        print "selected_time",self.selected_time

    def fit(self, robot):
        #print self.desfasaje_rotacion
        if self.desfasaje_rotacion:
            return False

        collideds = pygame.sprite.spritecollide(self, robot, False)
        pprint(collideds)
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

    def count(self, x=0):
        i = self._velocity()
        x = x
        while 1:
            x = x+i
            yield x

class Pieces(object):
    def __init__(self, level, static=False):
        self.level = level
        self.images = self.load_images()
        self.static = static

    def load_images(self):
        result = []
        for pathfile in glob.glob(os.path.join(PIECES_LEVEL[self.level], '*.png')):
            myFile = os.path.basename(pathfile)
            myId = myFile[:-4]
            image = utils.load_image_alpha(pathfile, -1)
            result.append((int(myId), image))
        return result

    def get_all(self):
        result = []
        for img in self.images:
            piece = Piece(img[0], img[1], self.level, self.static)
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

        self.npiezas = 0
        self.mouse_with_piece = False

    def selected_explosion(self):
        self.selected_piece.selected = False
        self.mouse_with_piece = False
        self.piezas_activas.remove(self.selected_piece)
        ExplosionMedium(self.selected_piece.rect.center)
        self.selected_piece.set_top_position()

    def new_dispatch(self):
        if not self.piezas_activas.sprites():
            return True

        for p in self.piezas_activas:
            if p.rect.top < HEIGHT:
                return False
        return True

    def dispatch(self):
        if self.new_dispatch():
            self.piezas_activas.empty()

            options = self.piezas.sprites()
            for i in range(self.mount):
                if options:
                    pieza = random.choice(options)
                    options.remove(pieza)
                    pieza.set_top_position()
                    self.piezas_activas.add(pieza)
                    print pieza.id

    def rotate_selected(self, angle):
        if self.mouse_with_piece:
            self.selected_piece.rotate(angle)

    def agarrar_soltar(self, pos):
        '''Logica para agarrar o soltar las piezas con el mouse'''
        for piece in self.piezas:
            if piece.rect.collidepoint(pos):
                self.selected_piece = piece

                #Primer click (agarrar)
                if not self.mouse_with_piece:
                    self.mouse_with_piece = True
                    piece.select(1500)
                #Segundo Click (soltar)
                else:
                    self.mouse_with_piece = False
                    piece.selected = False
                    piece.release()

                    if self.selected_piece.fit(self.robot):

                        print "ENCAJO!!"
                        self.piezas_encajadas.add(self.selected_piece)

                        self.npiezas += 1

                        self.piezas.remove(self.selected_piece)
                        self.piezas_activas.remove(self.selected_piece)
                break
            

if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces(level=1)
    print pieces.get_all()
