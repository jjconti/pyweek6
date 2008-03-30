import pygame
import data
from config import *
import os
import glob
import utils
from levelposimages import *
#from pygame.locals import *
#from config import *
import math
import random

class Piece(pygame.sprite.Sprite):
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2)]
    def __init__(self, id, img):
        self.id = id
        self.selected = False
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = level1[id]
        self.min_vel, self.max_vel = 0,0#self._velocity()
        self.num = self.count(self.min_vel, self.max_vel)
        self.func_x = random.choice(self.functions)
        cordenates = range(HEIGHT) # alto
        self.x = random.choice(cordenates)
        self.y = random.choice(cordenates)

    def _velocity(self):
        largo, ancho = self.rect.size
        return (largo * ancho) / float(500) + 2

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
                self.rect.move_ip(0, pos[1])
                self.num = self.count(self.min_vel, self.max_vel)
                self.y = 0

    def count(self, min_vel, max_vel):
        #i = random.randrange(min_vel, max_vel)
        i = self._velocity()
        x = 0
        while 1:
            x = x+i
            yield x

class Pieces():
    def __init__(self):
        self.images = self.load_images()

    def load_images(self):
        result = []
        #print PIECES_LEVEL1
        for pathfile in glob.glob(os.path.join(PIECES_LEVEL1, '*.png')):
            #print filename
            image = utils.load_image(pathfile)
            result.append(image)
        return result

    def get_all(self):
        result = []
        for id, img in enumerate(self.images):
            piece = Piece(id+1, img)
            result.append(piece)
        return result



if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces()
    print pieces.get_all()
