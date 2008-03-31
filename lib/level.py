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
        
        self.explosions = pygame.sprite.Group()
        ExplosionMedium.containers = self.explosions

        #Create the game clock
        self.clock = pygame.time.Clock()
        self.cargar_robot()
        self.npiezas = 0
        self.totalpiezas = len(self.robot)
        self.mouse_with_piece = False

        self.cargar_piezas()

    def loop(self):  
        #music.play_music(PLAYMUSIC)
        while not self.finish():
            self.tics += 1
   
            if not self.paused:
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
        self.piezas.update()
        self.explosions.update()

    def draw(self):
        self.screen.blit(utils.create_surface((WIDTH, HEIGHT), (100,100,100)), (0,0) )
        self.robot.draw(self.screen)
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
                self.agarrar_soltar(event.pos)

            if event.button == 2:
                ExplosionMedium(event.pos)

            if event.button == 4:
                if self.mouse_with_piece:
                    self.selected_piece.rotate(90)

            if event.button == 5:
                if self.mouse_with_piece:
                    self.selected_piece.rotate(270)

    def agarrar_soltar(self, pos):
        '''Logica para agarrar o soltar las piezas con el mouse'''
        for piece in self.piezas:
            if piece.rect.collidepoint(pos):
                self.selected_piece = piece

                #Primer click (agarrar)
                if not self.mouse_with_piece:
                    self.mouse_with_piece = True
                    piece.selected = True
                #Segundo Click (soltar)
                else:
                    self.mouse_with_piece = False
                    piece.selected = False
                    #print 'llama a release'
                    piece.release()
                    #piece.x, piece.y = piece.rect.topleft

                    if self.selected_piece.fit(self.robot):
                        self.npiezas += 1
                        self.robot.add(self.selected_piece)
                        self.piezas.remove(self.selected_piece)
                break

    def finish(self):
        return self.totalpiezas == self.npiezas

    def cargar_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces(static=True, level=self.level)

        self.robot = pygame.sprite.RenderUpdates(p.get_all())


    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas = pygame.sprite.RenderUpdates(sprites)

        #for piece in self.piezas:
            #piece.image = piece.image.convert_alpha()

def main():
    Level().loop()

if __name__ == "__main__py":
    main()
