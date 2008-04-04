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
import random

##
# Módulos propios
from config import *


class Credits(object):
    def __init__(self, screen, father=None):
        self.flag = True
        self.screen = screen
        self.father = father
        self.font = self._generate_fontSize()
        self.developers = [self._generate_images(name) for name in self._load_credits()]

    def loop(self):
        pygame.event.clear()
        while self.flag:
            if self._verifyKey():
                self.flag = False
            self._draw_screen()
        return self.father

    def _generate_fontSize(self):
        """Crea la lista de tamaños de fuentes y la fuente en sí"""
        #base = 10
        sizes = [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        lista_size = []
        for num in range(16):
            lista_size.append(num*sizes[num])
            #base+=1
        """
        lista_size.append(base+10)
        self.punto_medio = lista_size.index(base+10)
        base-=5
        for num in range(8):
            lista_size.append(base)
            base-=5
        """
        lista_font = []
        # Gereramos las fuentes
        for size in lista_size:
            lista_font.append(pygame.font.Font(FONT_CREDITS, size))
        return lista_font

    def _load_credits(self):
        list_name = []
        try:
            credits = csv.reader(open(CREDITS))
            list_aux = []
            for pos, credit in enumerate(credits):
                if 0 < pos < 8 and len(credit) == 2:
                    list_aux.append(credit)
                elif pos == 8:
                    random.shuffle(list_aux)
                    for gente in list_aux:
                        list_name.append(gente)
                    list_name.append(credit)
                else:
                    list_name.append(credit)
            list_aux = list_name
            list_name = []
            for developer in list_aux:
                developer = ' '.join(developer)
                list_name.append(developer)
        except IOError:
            print 'Cannot open credits file'
        return list_name

    def _generate_images(self, developer):
        list_name = []
        for font in self.font:
            list_name.append(font.render(developer, True, GREY))
        return list_name

    def _verifyKey(self):
        if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == KEYDOWN and \
                    (event.key in [K_ESCAPE, K_RETURN, K_KP_ENTER]):
                    return True
        return False

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
        while self.flag:
            for name in self.developers:
                self._dibujar_secuencia(name, background, topleft)
                if self._verifyKey():
                    self.flag = False
                    break

# ****************************************************************************************************

    def _dibujar_secuencia(self, lista_imagenes, background, topleft):
        """Permitirá mostrar las letras en la secuencia de descenso"""
        y = (WIDTH / 2) - 300 
        print y
        bandera = False
        cambiar = False
        clock = pygame.time.Clock()
        time_loop = 0
        while not bandera:
            clock.tick(CLOCK_TICS)
            if self._verifyKey():#FIXME
                self.flag = False
                return
            pygame.display.flip()
            self.screen.blit(background, (0,0))
            time_loop+=1
            if cambiar or time_loop==1000:#y >= 780 or time_loop == 1000:
                bandera = True
            else:
                if self._verifyKey():#FIXME
                    self.flag = False
                    return
                for pos, font in enumerate(lista_imagenes):
                    if self._verifyKey():
                        self.flag = False
                        return
                    self.screen.blit(background, (0,0))
                    pos_x_inicial = (WIDTH / 2 - font.get_width() / 2)
                    self.screen.blit(font, (pos_x_inicial, y))
                    pygame.time.delay(80)
                    y += font.get_height() - 50
                    pygame.display.flip()
                    cambiar = True
                pygame.time.delay(1000)

# ****************************************************************************************************

if __name__ == '__main__':
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    credits = Credits(screen)
    credits.loop()
