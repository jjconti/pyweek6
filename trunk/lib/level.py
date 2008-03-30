#! -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from pieces import Pieces
from config import *

import utils

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Level(object):
    '''Ojalata level'''

    def __init__(self, screen, father, level=1, total_points=0):

        self.screen = screen
        self.father = father
        self.level = level
        #self.background = utils.load_image(levels[level]['background'])
        self.tics = 0
        self.exit = False
        #Create the game clock
        self.clock = pygame.time.Clock()
        self.cargar_robot()
        

        self.mouse_with_piece = False

        self.cargar_piezas()


    def loop(self):  
        #music.play_music(PLAYMUSIC)
        while not self.finish():
            self.tics += 1            
   
            #self.screen.blit(self.background, (0,0)) 
            self.update()
            self.draw()

            #Control
            for event in pygame.event.get():
                self.control(event)

            self.clock.tick(CLOCK_TICS)

            pygame.display.flip()
    
        if self.exit:
            return self.father

    def update(self):
        '''Actualizar valores de variables y ejecuta los update()
           de los grupos.'''
        self.piezas.update()

    def draw(self):
        self.screen.blit(utils.create_surface((WIDTH, HEIGHT), (0,0,0)), (0,0) )
        self.robot.draw(self.screen)
        '''Dibuja en pantalla los grupos.'''
        self.piezas.draw(self.screen)

    def control(self, event):
        
        if event.type == QUIT:
            sys.exit(0)
	    
	if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for piece in self.piezas:
                    if piece.rect.collidepoint(event.pos):
                        if not self.mouse_with_piece:
                            self.mouse_with_piece = True
                            piece.selected = True
                        else:
                            self.mouse_with_piece = False
                            piece.selected = False
                            piece.x, piece.y = piece.rect.topleft

            print "mouse"
            print event.button
            print event.pos

    def finish(self):
        return False

    def cargar_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces()
        self.robot = pygame.sprite.RenderUpdates(p.get_all())


    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces() for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas = pygame.sprite.RenderUpdates(sprites)

def main():
    Level().loop()

if __name__ == "__main__py":
    main()
