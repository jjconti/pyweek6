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
from config import FONT_CREDIT, CREDITS, WINDOW_TITLE


class Credits(object):
    def __init__(self, screen, father=None):
        self.screen = screen
        self.father = father
        self.credits = []
        self.font_1 = pygame.font.Font(FONT_CREDIT, 20)
        self.font_2 = pygame.font.Font(FONT_CREDIT, 40)
        self.font_3 = pygame.font.Font(FONT_CREDIT, 60)

    def loop(self):
        pygame.event.clear()
        #music.stop_music()
        #music.play_music(CREDITSMUSIC)
        self._load_credits()
        self._draw_screen()
        pygame.time.delay(200)
        #music.stop_music()
        return self.father
    
    def _load_credits(self):
        try:
            credits = csv.reader(open(CREDITS))
            for credit in credits:
                self.credits.append(credit)
            self._developers()
        except IOError:
            print 'Cannot open credits file'

    def _draw_screen(self):
        pygame.display.set_caption(WINDOW_TITLE)
        image = '/home/nercof/Proyectos/pyweek6/data/imgs/credits.png'
        background = pygame.image.load(image)

        clock = pygame.time.Clock()
        separator = 3

        title = 'CREDITS'
        title_img = self.font_3.render(title, True, (100, 100, 100))
        topleft = (background.get_rect().width - title_img.get_rect().width) / 2, 30
        background.blit(title_img, topleft)
    
    def _developers(self):
        print self.credits

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
