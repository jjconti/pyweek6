import pygame
import data
from config import *
import os
import glob
import utils
from levelposimages import *
import math
import random

class Piece(pygame.sprite.Sprite):
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2)]
    def __init__(self, id, img, static=False):
        self.id = id
        self.selected = False
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.static = static
        if self.static:
            self.rect.topleft = level1[id]
        else:
            self.min_vel, self.max_vel = 0,0#self._velocity()
            self.num = self.count(self.min_vel, self.max_vel)
            self.func_x = random.choice(self.functions)
            cordenates = range(HEIGHT) # alto
            angle = random.choice([90, 180, 270])
            self.rotate(angle)
            self.x = random.choice(cordenates)
            self.y = random.choice(cordenates)

        cordenates = range(HEIGHT) # alto

        if self.static:
            print level1[id]
            self.rect.topleft = level1[id]
        else:
            self.min_vel, self.max_vel = 0,0#self._velocity()
            self.num = self.count(self.min_vel, self.max_vel)
            self.func_x = random.choice(self.functions)
            cordenates = range(HEIGHT) # alto
            self.x = random.choice(cordenates)
            self.y = random.choice(cordenates)
            self.rect.topleft = (random.choice(cordenates), random.choice(cordenates))

        self.min_vel, self.max_vel = 0,0#self._velocity()
        self.num = self.count(self.min_vel, self.max_vel)
        self.func_x = random.choice(self.functions)
        
        self.x = random.choice(cordenates)
        self.y = random.choice(cordenates)

    def _velocity(self):
        largo, ancho = self.rect.size
        return (largo * ancho) / float(500) + 2
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect()
    
    def fit(self, robot):
        collideds = pygame.sprite.spritecollide(self, robot, False)
        target = [x for x in collideds if x.id == self.id ]
        if target:
            self.rect.topleft = target[0].rect.topleft
            return True
        
        return False

    def update(self):
        if self.static:
            return
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
    def __init__(self, static=False):
        self.images = self.load_images()
        self.static = static

    def load_images(self):
        result = []
        #print PIECES_LEVEL1
        for pathfile in glob.glob(os.path.join(PIECES_LEVEL1, '*.png')):
            print pathfile
            image = utils.load_image(pathfile, -1)
            result.append(image)
        return result

    def get_all(self):
        result = []
        for id, img in enumerate(self.images):
            piece = Piece(id+1, img, self.static)
            result.append(piece)
        return result



if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    pieces = Pieces()
    print pieces.get_all()
