import pygame
import data
from config import *
import os
import glob
import utils
#from pygame.locals import *
#from config import *
#import math
#import random

class Piece(pygame.sprite.Sprite):
    def __init__(self, id, img):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

class Pieces():
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2)]

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
