#!/usr/bin/env python
# -*-coding: utf-8 -*-
# Filename: level.py

import sys
from pprint import pprint

import pygame
from pygame.locals import *

from config import *
import utils

from pieces import Pieces
from pieces import Dispatcher

from explosion import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Level(object):
    '''Ojalata level'''

    def __init__(self, screen, father, level=1, total_points=0):

        self.screen = screen
        self.father = father
        self.level = level
        self.tics = 0
        self.exit = False
        self.paused = False
        
        self.robot           = pygame.sprite.RenderUpdates()
        self.cargar_robot()
        self.piezas          = pygame.sprite.RenderUpdates()
        self.cargar_piezas()
        self.piezas_erroneas = pygame.sprite.Group()
        self.cargar_piezas_erroneas()
        self.piezas_activas  = pygame.sprite.Group()
        self.piezas_encajadas= pygame.sprite.Group()
        self.explosions      = pygame.sprite.Group()
        ExplosionMedium.containers = self.explosions

        #Create the game clock
        self.clock = pygame.time.Clock()
        self.dispatcher = Dispatcher(2, self.piezas_activas, self.piezas, self.piezas_erroneas, self.piezas_encajadas, self.robot)
        
        self.totalpiezas = len(self.robot)
        

    def loop(self):  
        #music.play_music(PLAYMUSIC)
        while not self.finish():
            self.tics += 1
   
            if not self.paused:
                self.dispatcher.dispatch()
                self.update()
                self.draw()

            #Control
            for event in pygame.event.get():
                self.control(event)

            self.clock.tick(CLOCK_TICS)

            pygame.display.flip()
    
        if self.level < 3:
            def f(screen):
                return Level(screen, self.father, self.level + 1)
            return f
        if self.exit:
            return self.father

    def update(self):
        '''Actualizar valores de variables y ejecuta los update()
           de los grupos.'''
        self.piezas_activas.update()
        self.explosions.update()

    def draw(self):
        self.screen.blit(utils.create_surface((WIDTH, HEIGHT), (100,100,100)), (0,0) )
        self.robot.draw(self.screen)
        self.piezas_encajadas.draw(self.screen)
        '''Dibuja en pantalla los grupos.'''
        self.piezas.draw(self.screen)
        self.explosions.draw(self.screen)
        

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)

        if event.type == KEYDOWN:
            if event.key == K_f:
                pygame.display.toggle_fullscreen()
            if event.key == K_p:
                self.paused ^= True	
        
	if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dispatcher.agarrar_soltar(event.pos)

            if event.button == 2:
                ExplosionMedium(event.pos)

            if event.button == 4:
                self.dispatcher.rotate_selected(90)

            if event.button == 5:
                self.dispatcher.rotate_selected(270)

    def finish(self):
        return self.totalpiezas == self.dispatcher.npiezas

    def cargar_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces(static=True, level=self.level)

        self.robot.add(p.get_all())

        for piece in self.robot:
            piece.image = piece.image.convert()
            piece.image.set_colorkey((255,255,255), RLEACCEL)
            piece.image.set_alpha(50)



    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas.add(sprites)

    
    def cargar_piezas_erroneas(self):
        pass
        
def main():
    Level().loop()

if __name__ == "__main__py":
    main()
