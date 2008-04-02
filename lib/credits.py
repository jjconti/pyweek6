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
from config import GREY


class Credits(object):
    def __init__(self, screen, father=None):
        self.screen = screen
        self.father = father
        self.developers = []
        self.font = []
        for x in xrange(2,5):
            print x*10
            self.font.append(pygame.font.Font(FONT_CREDIT, x*10))

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
        except IOError:
            print 'Cannot open credits file'

    def _generar_imagenes(self, developer):
        """Genero por cada tamaño de letra una cantidad de palabras para ir
        mostrandolas en el mismo tiempo en distintas coordenadas"""
        lista = {}
        for pos, font in enumerate(self.font):
            lista[pos] = []
            for obj in range(3):
                lista[pos].append(font.render(developer, True, GREY))
        return lista

    def _dibujar_secuencia(self, lista_imagenes, background, topleft):
        """Permitirá mostrar las letras en la secuencia de descenso"""
        pos_x_inicial = 348
        pos_y = y = topleft[1] + 50
        bandera = False
        clock = pygame.time.Clock()
        time_loop = 0
        while not bandera:
            clock.tick(1000)
            pygame.display.flip()
            self.screen.blit(background, (0,0))
            time_loop += 1
            if time_loop == 1000:
                bandera = True
            if self._verifyKey():
                return self.father #FIXME
            if y >= 160:
                # Poner imagen_2
                for pos, font in enumerate(lista_imagenes[1]):
                    self.screen.blit(lista_imagenes[1][pos],
                            (pos_x_inicial, y))
                #pygame.time.delay(50)
                #pass
                y += 2
            elif y >= 190:
                # Poner imagen_3
                for pos, font in enumerate(lista_imagenes[2]):
                    self.screen.blit(lista_imagenes[2],
                            (pos_x_inicial, y))
                y +=2
                #pygame.time.delay(100)
            else:
                # Palabras pequeñas
                for pos, font in enumerate(lista_imagenes[0]):
                    self.screen.blit(lista_imagenes[0][pos],
                            (pos_x_inicial, y))
                y += 2

    def _draw_screen(self):
        pygame.display.set_caption(WINDOW_TITLE)
        image = IMAGE_CREDITS
        background = pygame.image.load(image)

        title = 'CREDITS'
        title_img = self.font[-1].render(title, True, (100, 100, 100))
        topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        background.blit(title_img, topleft)
        self.screen.blit(background, (0,0))
        pygame.display.flip()

        # Probemos con dos nomas
        lista_aux = self.developers[1:4]
        while True:
            for developer in lista_aux:#self.developers[0:2]:
                developer = ' '.join(developer)
                # genero las imagenes para mostrar
                lista_imagenes = self._generar_imagenes(developer)
                self._dibujar_secuencia(lista_imagenes, background, topleft)

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
