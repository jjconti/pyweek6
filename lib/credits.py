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
from config import *


class Credits(object):
    def __init__(self, screen, father=None):
        self.screen = screen
        self.father = father
        print "Padre: ", self.father
        self.developers = []
        self.font = []
        self.font = self.generar_fuentes()

    def generar_fuentes(self):
        """Crea la lista de tamaños de fuentes y la fuente en sí"""
        base = 10
        lista_size = []
        for num in range(8):
            lista_size.append(base)
            base+=5
        lista_size.append(base+10)
        self.punto_medio = lista_size.index(base+10)
        base-=5
        for num in range(8):
            lista_size.append(base)
            base-=5
        print "Lista size: ", lista_size
        lista_font = []
        # Gereramos las fuentes
        for size in lista_size:
            lista_font.append(pygame.font.Font(None, size))
        return lista_font

    def loop(self):
        pygame.event.clear()
        self._load_credits()
        self._draw_screen()

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
        lista = []
        for font in self.font:
            lista.append(font.render(developer, True, GREY))
        return lista

    def _dibujar_secuencia(self, lista_imagenes, background, topleft):
        """Permitirá mostrar las letras en la secuencia de descenso"""
        pos_y = y = topleft[1] + 50
        bandera = False
        cambiar = False
        clock = pygame.time.Clock()
        time_loop = 0
        while not bandera:
            clock.tick(1000)
            pygame.display.flip()
            self.screen.blit(background, (0,0))
            time_loop+=1
            if cambiar or time_loop==1000:#y >= 780 or time_loop == 1000:
                bandera = True
            else:
                if self._verifyKey():#FIXME
                    print "Quiero salir!"
                    return self.father
                for pos, font in enumerate(lista_imagenes):
                    pos_x_inicial = (400 - font.get_width() / 2)
                    #print "Pos_x_inicial: ", pos_x_inicial
                    #pos_x_inicial = (WIDTH - font.get_width() / 2)-100
                    self.screen.blit(font, (pos_x_inicial, y))
                    if pos == self.punto_medio:
                        pygame.time.delay(1000)
                    #pygame.time.delay(100)
                    y += font.get_height()
                    pygame.display.flip()
                    cambiar = True
                pygame.time.delay(1000)

    def _draw_screen(self):
        pygame.display.set_caption(WINDOW_TITLE)
        image = IMAGE_CREDITS
        background = pygame.image.load(image)

        title = 'CREDITS'
        title_img = self.font[7].render(title, True, (100, 100, 100))
        topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        background.blit(title_img, topleft)
        self.screen.blit(background, (0,0))
        pygame.display.flip()

        # Probemos con dos nomas
        lista_aux = self.developers
        while True:
            for developer in lista_aux:
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
    print "Paso algo..."
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    credits = Credits(screen)
    credits.loop()
