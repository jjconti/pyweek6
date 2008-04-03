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

from levelposimages import *

class StaticPiece(pygame.sprite.Sprite):
    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = self._image(img)
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id

        self.set_position()
        
    def _image(self, img):
        img = img.convert()
        img.set_colorkey((255,255,255), RLEACCEL)
        img.set_alpha(50)
        return img

    def set_position(self):
        t,l = level_pos[self.level][self.id][:2]
        self.rect.topleft = t + ROBOT_OFFSET[0], l + ROBOT_OFFSET[1]
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.image.set_alpha(50)

    def __str__(self):
        return "Pieza %d" % (self.id,)

class MiniRobotPiece(pygame.sprite.Sprite):
    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)
	self.factor = .4
	(w, h) = img.get_width() * self.factor, img.get_height()* self.factor
        self.image = pygame.transform.scale(img, (w, h))
        self.image = self.fill_no_alpha((0, 255, 0))
        self.selected_image = self.fill_no_alpha((0, 0, 0))

        self.rect = self.image.get_rect()
        self.level = level
        self.id = id

        self.set_position()

    def set_position(self):
        t,l = level_pos[self.level][self.id][:2]
        self.rect.topleft = self.factor*t + MINI_ROBOT_OFFSET[0], self.factor*l + MINI_ROBOT_OFFSET[1]
        self.image = self.image.convert()


    def fill_no_alpha(self, color):
        temp = self.image.copy()
        for w in range(temp.get_width()):
            for h in range(temp.get_height()):
                if temp.get_at((w, h))[:3] != (255,255,255):
                    temp.set_at((w, h), color) 

        temp = temp.convert()
        temp.set_colorkey((255,255,255), RLEACCEL)
        temp.set_alpha(100)
        return temp

    def select(self):
        self.image = self.selected_image

    def __str__(self):
        return "Pieza %d" % (self.id,)

class FacePiece(StaticPiece):

    def set_position(self):
        t,l = level_pos[self.level][2][:2]  #2 es la cara en todos los niveles
        self.rect.topleft = t + ROBOT_OFFSET[0] + 15, l + ROBOT_OFFSET[1] + 10


class DinamicPiece(pygame.sprite.Sprite):
    functions = [lambda x,direccion: direccion*20*math.sin(x/2),
                 lambda x,direccion: direccion*20*math.cos(x/2),
                 lambda x,direccion: direccion*x,
                 lambda x,direccion: direccion*x**2/6,
                 lambda x,direccion: -direccion*x**2/6]

    MOVING_CINTA   = 0
    MOVING_NORMAL  = 1
    MOVING_FALLING = 2
    MOVING_STOP    = 3

    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id
        self.selected = False
        self.selected_time = 0
        self.desfasaje_rotacion = 0
        self.moving = self.MOVING_STOP
        self.prof = level_pos[self.level].get(self.id, False)
        if self.prof:
            self.prof = self.prof[2] # Fix
        self.set_top_position()
        self.change_function = random.choice(range(HEIGHT))

    def is_wrong(self):
        return not (1 <= self.id <= 50)

    def release(self):
        music.stop_peep()
        self.selected = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.num = self.count()
        self.x = mouse_x
        self.y = mouse_y
        self.moving = self.MOVING_FALLING

    def select(self, miliseconds=2000):
        music.play_peep()
        self.selected = True
        self.selected_time = (miliseconds * CLOCK_TICS) / 1000

    def fit(self, robot, mini_robot):
        if self.desfasaje_rotacion:
            return False

        collideds = pygame.sprite.spritecollide(self, robot, False)

        target = [x for x in collideds if x.id == self.id ]

        if target:
            self.rect.topleft = target[0].rect.topleft
	    mini_robot_piece = [x for x in mini_robot if x.id == self.id][0]
            mini_robot_piece.select()
            return True
        return False

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
        self.rect.bottom = 0

    def _velocity(self):
        #largo, ancho = self.rect.size
        #vel = (largo * ancho) / float(500) + 2
        #return min(50, vel)
        return random.choice(range(20, 35))

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect()
        self.desfasaje_rotacion = (self.desfasaje_rotacion + angle) % 360

    def update(self):

        if self.moving == self.MOVING_STOP:
            return

        if self.rect.bottom > HEIGHT - 20:
            self.moving = self.MOVING_CINTA

        if self.rect.left > WIDTH:
            self.moving = self.MOVING_STOP

        if self.selected:
            self.rect.center   = pygame.mouse.get_pos()
            self.selected_time -= 1
            if self.selected_time == 0:
                self.dispatcher.selected_explosion()
        else:
            if self.moving == self.MOVING_CINTA:
                self.update_cinta()
            elif self.moving == self.MOVING_NORMAL:
               self.update_normal()
            elif self.moving == self.MOVING_FALLING:
               self.update_falling()

    def update_cinta(self):
        self.rect.left += 4

    def update_falling(self):
        self.rect.top += 5

    def update_normal(self):
        if self.rect.y == self.change_function:
            self.func_x = random.choice(self.functions)

        num = self.num.next()
        num = math.radians(num)
        func_y = 10*num

        direccion = 1
        pos = (self.func_x(num,direccion) + self.x, func_y + self.y)
        self.rect.center = pos
        if self.rect.top > HEIGHT:
            self.rect.move_ip(0, pos[1])
            self.num = self.count()
            self.y = 0

    def is_moving(self):
        return self.moving in (self.MOVING_NORMAL, self.MOVING_CINTA, self.MOVING_FALLING)

    def is_falling(self):
        return self.moving in (self.MOVING_NORMAL, self.MOVING_FALLING)

    def move(self):
        self.moving = self.MOVING_NORMAL

    def count(self, x=0):
        i = self._velocity()
        x = x
        while 1:
            x = x+i
            yield x

class GoldenPiece(DinamicPiece):

    MOVING_CINTA   = 0
    MOVING_NORMAL  = 1
    MOVING_FALLING = 2
    MOVING_STOP    = 3

    def __init__(self, id, img, level):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        self.level = level
        self.id = id
        self.selected = False
        self.selected_time = 0
        self.desfasaje_rotacion = 0
        self.moving = self.MOVING_STOP
        self.prof = level_pos[self.level].get(self.id, False)
        if self.prof:
            self.prof = self.prof[2] # Fix
        self.set_top_position()
        self.change_function = random.choice(range(HEIGHT))

class Pieces(object):
    def __init__(self, level, type_piece="static"):
        self.level = level
        self.type_piece = type_piece
        self.images = self.load_images()

    def load_images(self):
        if self.type_piece in ("static", "dinamic", "mini_robot"):
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
        elif self.type_piece == "golden":
            result = []
            for pathfile in glob.glob(os.path.join(GOLDEN_LEVEL[self.level], '*.png')):
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
            elif self.type_piece == "mini_robot":
                piece = MiniRobotPiece(img[0], img[1], self.level)
            elif self.type_piece in ("dinamic", "erronea"):
                piece = DinamicPiece(img[0], img[1], self.level)
            elif self.type_piece == "golden":
                piece = GoldenPiece(img[0], img[1], self.level)
            elif self.type_piece == "face":
                piece = FacePiece(img[0], img[1], self.level)
            result.append(piece)
        return result


if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces(level=1)
