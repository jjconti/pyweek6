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
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        pass

class Pieces():
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2)]

    def __init__(self):
        self.pieces = self.load_images()

    def load_images(self):
        result = []
        print PIECES_LEVEL1
        for filename in os.listdir(PIECES_LEVEL1):
            print filename
            image = utils.load_image(os.path.join(PIECES_LEVEL1, filename))
            result.append(image)
        return result


if __name__ == '__main__':
    pieces = Pieces()
    print pieces.load_images()
