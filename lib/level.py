#!/usr/bin/env python
# -*-coding: utf-8 -*-
# Filename: level.py

import sys
from pprint import pprint
import time

import pygame
from pygame.locals import *

from config import *
import utils

from pieces import Pieces
from pieces import Dispatcher
from pieces import EnergyBar

from explosion import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Level(object):
    '''Ojalata level'''

    def __init__(self, screen, father, level=1, total_points=0):

        self.screen = screen
        self.background = utils.load_image(BACK)
        self.father = father
        self.level = level
        self.tics = 0
        self.exit = False
        self.paused = False
        
        self.robot = pygame.sprite.RenderUpdates()
        self.cargar_robot()
        self.piezas = pygame.sprite.RenderUpdates()
        self.cargar_piezas()
        self.piezas_erroneas = pygame.sprite.RenderUpdates()
        self.cargar_piezas_erroneas()
        self.piezas_activas  = pygame.sprite.Group()
        self.piezas_encajadas= pygame.sprite.Group()
        self.widgets = pygame.sprite.Group()
        self.widgets.add(EnergyBar())
        self.explosions = pygame.sprite.Group()
        ExplosionMedium.containers = self.explosions
        #self.face = pygame.sprite.GroupSingle()
        self.face = pygame.sprite.RenderUpdates()
        self.last_face = None
        self.cargar_faces()
        self.situacion = ""
        self.facetime = time.time()
        #Create the game clock
        self.clock = pygame.time.Clock()
        self.dispatcher = Dispatcher(3, self.piezas_activas, self.piezas, \
                                     self.piezas_erroneas, \
                                     self.piezas_encajadas, self.robot)
        
        
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
        self.widgets.update()

    def draw(self):
        self.screen.blit(self.background, (0,0) )
        self.robot.draw(self.screen)
        self.piezas_encajadas.draw(self.screen)
        self.face.draw(self.screen)
        '''Dibuja en pantalla los grupos.'''
        self.piezas_activas.draw(self.screen)
        self.explosions.draw(self.screen)
        self.widgets.draw(self.screen)


    def control(self, event):
        if event.type == KEYDOWN:
            if event.key == K_f:
                pygame.display.toggle_fullscreen()
            if event.key == K_p:
                self.paused ^= True

        if self.paused:
            return

        if event.type == QUIT:
            sys.exit(0)

        if event.type == MOUSEMOTION:
            self.face_change(event)

        if event.type == KEYDOWN:
            if event.key == K_f:
                pygame.display.toggle_fullscreen()
            if event.key == K_DOWN:
                self.dispatcher.rotate_selected(90)
            if event.key == K_UP:	
                self.dispatcher.rotate_selected(270)       

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                quepaso = self.dispatcher.agarrar_soltar(event.pos)
                self.face_change(event, quepaso)

            if event.button == 2:
                ExplosionMedium(event.pos)

            if event.button == 4:
                self.dispatcher.rotate_selected(90)

            if event.button == 5:
                self.dispatcher.rotate_selected(270)

    def finish(self):
        return not self.piezas.sprites()

    def cargar_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces(type_piece="static", level=self.level)

        self.robot.add(p.get_all())

        for piece in self.robot:
            piece.image = piece.image.convert()
            piece.image.set_colorkey((255,255,255), RLEACCEL)
            piece.image.set_alpha(50)

    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(type_piece="dinamic", level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas.add(sprites)

    def cargar_piezas_erroneas(self):
        sets = [Pieces(type_piece="erronea", level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas_erroneas.add(sprites)

    def cargar_faces(self):
        sets = [Pieces(type_piece="face", level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.face_list = sprites
        feliz = [f for f in self.face_list if f.id == FELIZ3][0]
        self.face.add(feliz)
        self.last_face = feliz

    def face_change(self, event, quepaso=""):
        '''Captura el movimiento del mouse para cambiar la cara del robot.'''
        x,y = event.pos        
        limit1 = ROBOT_OFFSET[1] + 150
        if quepaso: self.situacion = quepaso
        
        if self.situacion == "correcto" and y < limit1 and self.face.sprites()[0].id != INCERTIDUMBRE:
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == INCERTIDUMBRE])

        elif self.situacion == "correcta" and y >= limit1:
            self.face.empty()
            self.face.add(self.last_face)

        elif self.situacion == "encajo":
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == FELIZ])

        elif self.situacion == "soltoafuera":
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == SORPRESA])

        elif self.situacion == "clickafuera":
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == MIEDO])

        elif self.situacion == "erronea" and self.face.sprites()[0].id != SORPRESA:
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == SORPRESA])
            self.facetime = time.time()
            self.situacion = "volver"
    
        elif self.situacion == "volver": # ciertas caras, luego de unos segundos vuelven a la anterior
            delay = time.time() - self.facetime
            
            if delay > 2:
                self.face.empty()
                self.face.add(self.last_face)
                self.situacion = ""


def main():
    Level().loop()

if __name__ == "__main__py":
    main()
