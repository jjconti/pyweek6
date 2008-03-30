import pygame
import data
from config import *
import os
import glob
import utils
from levelposimages import *
import random
import math
#from pygame.locals import *
#from config import *
#import math
#import random

class Piece(pygame.sprite.Sprite):
    functions = [lambda x: 20*math.sin(x/4),
                 lambda x: 20*math.cos(x/2)]

    def __init__(self, id, img):
        self.id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = level1[id]
        self.min_vel, self.max_vel = self._vel()
        self.num = self.count(self.min_vel, self.max_vel)
        self.func_x = random.choice(self.functions)
        cordenates = range(HEIGHT) # alto
        self.x = random.choice(cordenates)
        self.y = random.choice(cordenates)

    def _vel(self):
        largo, ancho = self.rect.size
        return 5, 6

    def update(self):
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
        i = random.randrange(min_vel, max_vel)
        x = 0
        while 1:
            x = x+i
            yield x

class Pieces():
    def __init__(self):
        self.images = self._load_images()
        self.pieces = self._gen_pieces()

    def _load_images(self):
        # carga todas las imagenes
        result = []
        for pathfile in glob.glob(os.path.join(PIECES_LEVEL1, '*.png')):
            image = utils.load_image(pathfile)
            result.append(image)
        return result

    def _gen_pieces(self):
        # crea las piezas y las agrega a un grupo
        result = []
        for id, img in enumerate(self.images):
            piece = Piece(id+1, img)
            result.append(piece)
        return result

    def get_all(self):
        # devuelve todas las piezas generadas
        return self.pieces

if __name__ == '__main__':
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    group = pygame.sprite.Group()

    pieces = Pieces()
    for piece in pieces.get_all():
        group.add(piece)

    #for x in range(150):
        #sprite = Piece(1,5)
        #group.add(sprite)

    #p = Piece(1, utils.load_image('/home/manuel/proyectos/pyweek6/data/imgs/level1/pieces/1.png'), 1, 50)
    #group.add(p)
    allsprites = pygame.sprite.RenderPlain(group)

    while 1:
        #for event in pygame.event.get():
            #if event.type == QUIT:
                #sys.exit(0)
            #elif event.type == KEYDOWN and event.key == K_ESCAPE:
                #sys.exit(0)

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

