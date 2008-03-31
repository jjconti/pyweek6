#!/usr/bin/env python
# -*-coding: utf-8 -*-
# Filename: pieces.py

import pygame
import data
from config import *
import os
import glob
import utils
from levelposimages import level_pos
import math
import random
from pprint import pprint
from pygame.locals import RLEACCEL

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
        self.desfasaje_rotacion = 0
        
        if static:
            self.rect.topleft = level_pos[self.level][id]
            self.image = self.image.convert()
            self.image.set_colorkey((255,255,255), RLEACCEL)
            self.image.set_alpha(50)
        else:
            self.num = self.count()
            self.func_x = random.choice(self.functions)
            angle = random.choice([90, 180, 270])
            self.rotate(angle)
            # define el rango de cordenadas en las que pueden aparecer las
            # piezas (cordenada y solamente, x aparecen en 0)
            cordenates = range(WIDTH) # alto
            self.x = random.choice(cordenates)
            self.y = 0#random.choice(cordenates)

    def _velocity(self):
        largo, ancho = self.rect.size
        vel = (largo * ancho) / float(500) + 2
        #print "Velocidad: ",vel
        return min(30, vel)
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect()
        self.desfasaje_rotacion = (self.desfasaje_rotacion + angle) % 360
        #print self.desfasaje_rotacion

    def release(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.num = self.count()
        self.x = mouse_x
        self.y = mouse_y

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

        if self.selected:
            self.rect.center = pygame.mouse.get_pos()

        else:
            num = self.num.next()
            num = math.radians(num)
            func_y = 10*num

            pos = (self.func_x(num) + self.x, func_y + self.y)
            self.rect.center = pos
            if self.rect.top > HEIGHT:
                #print self.num.next()
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

if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces(level=1)
    print pieces.get_all()
