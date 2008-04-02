#!/usr/bin/env python
# -*-coding: utf-8 -*-
# Filename: credits.py

##
# Módulos del sistema
import pygame
from pygame.locals import *
from time import sleep
import csv
import sys

##
# Módulos propios
from config import FONT_CREDIT, CREDITS, WINDOW_TITLE,IMAGE_CREDITS


class Credits(object):
    def __init__(self, screen, father=None):
        self.screen = screen
        self.father = father
        self.developers = []
        self.font_1 = pygame.font.Font(FONT_CREDIT, 30)
        self.font_2 = pygame.font.Font(FONT_CREDIT, 40)
        self.font_3 = pygame.font.Font(FONT_CREDIT, 60)

    def loop(self):
        pygame.event.clear()
        self._load_credits()
        self._draw_screen()
        pygame.time.delay(200)
        return self.father

    def _load_credits(self):
        try:
            credits = csv.reader(open(CREDITS))
            for credit in credits:
                self.developers.append(credit)
            self._developers()
        except IOError:
            print 'Cannot open credits file'

    def _draw_screen(self):
        pygame.display.set_caption(WINDOW_TITLE)
        image = IMAGE_CREDITS
        background = pygame.image.load(image)

        #title = 'CREDITS'
        #title_img = self.font_3.render(title, True, (100, 100, 100))
        #topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        #background.blit(title_img, topleft)
        #self.screen.blit(background, (0,0))
        #pygame.display.flip()
        clock = pygame.time.Clock()

        # Probemos con dos nomas
        lista_aux = self.developers[1:4]
        while True:
            for developer in lista_aux:#self.developers[0:2]:
                print "Viene ", developer
                bandera = False
                time_loop = 0
                pos_x_inicial = 250
                pos_y = y = 100#background.get_rect().width/2
                developer = ' '.join(developer)
                # genero las imagenes para mostrar
                imagen_1 = self.font_1.render(developer, True,
                        (100,100,100))
                imagen_2 = self.font_2.render(developer, True,
                        (100,100,100))
                imagen_3 = self.font_3.render(developer, True,
                        (100,100,100))

                while not bandera:
                    clock.tick(60)
                    pygame.display.flip()
                    self.screen.blit(background, (0,0))
                    time_loop += 1
                    if time_loop == 60:
                        bandera = True
                    if self._verifyKey():
                        return self.father
                    print 'Posicion Y: ', y
                    if y >= 190:
                        # Poner imagen_2
                        self.screen.blit(imagen_2, (pos_x_inicial, y))
                        pygame.time.delay(50)
                        #pass
                    elif y >= 220:
                        # Poner imagen_3
                        self.screen.blit(imagen_3, (pos_x_inicial, y))
                        pygame.time.delay(100)
                        #pass
                    else:
                        self.screen.blit(imagen_1, (pos_x_inicial, y)) # dibuja la imagen
                    y += 5

            pygame.time.delay(100)

    def _developers(self):
        print self.developers

    def _verifyKey(self):
        if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == KEYDOWN and \
                    (event.key in [K_ESCAPE, K_RETURN, K_KP_ENTER]):
                    return True
        return False

if __name__ == '__main__':
    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    credits = Credits(screen)
    credits.loop()
