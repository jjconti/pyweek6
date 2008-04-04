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

from dispatcher import Dispatcher
from pieces import *
from gadgets import *
from music import *
from explosion import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Level(object):
    '''Ojalata level'''

    def __init__(self, screen, father, level=1, points=0, t=5000):#t=5000):

        self.screen = screen
        pygame.mouse.set_visible(False)
        self.father = father
        self.level = level
        self.background = utils.load_image(BACKLEVEL[self.level])
        self.tics = 0
        self.totaltime = t
        self.exit = False
        self.paused = False

        self.robot = pygame.sprite.RenderUpdates()
        self.cargar_robot()
        self.mini_robot = pygame.sprite.RenderUpdates()
        self.cargar_mini_robot()
        self.piezas = pygame.sprite.RenderUpdates()
        self.cargar_piezas()
        self.golden_piezas_used = pygame.sprite.RenderUpdates()
        self.golden_piezas = pygame.sprite.RenderUpdates()
        self.cargar_golden_piezas()
        self.piezas_erroneas = pygame.sprite.RenderUpdates()
        self.cargar_piezas_erroneas()
        self.piezas_encajadas_atras = pygame.sprite.RenderUpdates()
        self.piezas_encajadas_adelante = pygame.sprite.RenderUpdates()
        self.energy_bar = EnergyBar()
        self.hand = Hand()
        #self.show_points = Points(0)
        self.indicator = Indicator(150, 90, 30)
        self.gadgets = pygame.sprite.RenderUpdates()
        self.gadgets.add(self.energy_bar)
        self.gadgets.add(self.hand)
        #self.gadgets.add(self.show_points)
        self.gadgets.add(self.indicator)
        self.face = pygame.sprite.RenderUpdates()
        self.last_face = None
        self.cargar_faces()
        self.explosions = pygame.sprite.RenderUpdates()
        ExplosionMedium.containers = self.explosions
        self.situacion = ""
        self.facetime = time.time()
        #Create the game clock
        self.clock = pygame.time.Clock()
        self.dispatcher = Dispatcher(3, self.piezas, self.golden_piezas, self.golden_piezas,  \
                                     self.piezas_erroneas, \
                                     self.piezas_encajadas_atras, self.piezas_encajadas_adelante,
                                     self.robot, self.mini_robot, self.hand)

        self.totalpiezas = len(self.robot)
        self.points = points
        self.bonus = 0
        self.alarm_play = False

    def loop(self):  
        #music.play_music(PLAYMUSIC)

        self.screen.blit(utils.load_image(CARTELBACKLEVEL[self.level]), (0,0))
        pygame.display.flip()
        pygame.time.delay(2000)
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


        if self.level == 1:     #pasamos al 2
            def f(screen):
                return Level(screen, self.father, self.level + 1, self.points, t=6500)
            return f
        elif self.level == 2:   #pasamos al 3
            def f(screen):
                return Level(screen, self.father, self.level + 1, self.points, t=7500)
            return f
        elif self.level == 3:   #fina del juego
            print "Ganaste"
            sys.exit()

        if self.exit:
            return self.father

    def update(self):
        '''Actualizar valores de variables y ejecuta los update()
           de los grupos.'''
        self.piezas.update()
        self.piezas_erroneas.update()
        self.golden_piezas.update()

        self.explosions.update()
        self.energy_bar.update(100 * (float(self.tics) / self.totaltime))
        if self.energy_bar.count() == 0:
            self.gameover()
        if self.totaltime - self.tics < CLOCK_TICS * 2 and not self.alarm_play:
            self.alarm_play = True
            play_alarm()
        self.hand.update()
        self.indicator.update(self.points, self.bonus, self.dispatcher.explosions)

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        self.robot.draw(self.screen)
	
        self.piezas_encajadas_atras.draw(self.screen)
        self.piezas_encajadas_adelante.draw(self.screen)
        self.face.draw(self.screen)
        '''Dibuja en pantalla los grupos.'''
        self.piezas.draw(self.screen)
        self.piezas_erroneas.draw(self.screen)
        self.golden_piezas.draw(self.screen)
        self.golden_piezas_used.draw(self.screen)

        self.explosions.draw(self.screen)
        self.gadgets.draw(self.screen)
        self.mini_robot.draw(self.screen)

    def control(self, event):
        if event.type == KEYDOWN:
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
                if quepaso == "encajo":
                    self.points += 10
                self.face_change(event, quepaso)

            if event.button == 2:
                ExplosionMedium(event.pos)
                print "Easter egg"

            if event.button == 4:
                self.dispatcher.rotate_selected(90)

            if event.button == 5:
                self.dispatcher.rotate_selected(270)

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.dispatcher.soltar()

    def finish(self):
        return not self.piezas.sprites()

    def cargar_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces(type_piece="static", level=self.level)
        self.robot.add(p.get_all())

    def cargar_mini_robot(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        p = Pieces(type_piece="mini_robot", level=self.level)
        self.mini_robot.add(p.get_all())

    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(type_piece="dinamic", level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas.add(sprites)
        
    def cargar_golden_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(type_piece="golden", level=self.level) for x in range(1)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.golden_piezas.add(sprites)

    def cargar_piezas_erroneas(self):
        sets = [Pieces(type_piece="erronea", level=self.level) for x in range(3)]
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
        limit1 = ROBOT_OFFSET[1] + 80
        if quepaso: self.situacion = quepaso

        if self.situacion == "correcta" and y < limit1 and self.face.sprites()[0].id != INCERTIDUMBRE:
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

        elif self.situacion == "clickafuera" and self.face.sprites()[0].id != MIEDO:
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == MIEDO])
            self.facetime = time.time()
            self.situacion = "volver"

        elif self.situacion == "erronea" and self.face.sprites()[0].id != SORPRESA:
            self.last_face = self.face.sprites()[0]
            self.face.empty()
            self.face.add([f for f in self.face_list if f.id == SORPRESA])
            self.facetime = time.time()
            self.situacion = "volver"

        elif self.situacion == "volver": # ciertas caras, luego de unos segundos vuelven a la anterior
            delay = time.time() - self.facetime

            if delay > 1:
                self.face.empty()
                self.face.add(self.last_face)
                self.situacion = ""

    def gameover(self):
        for p in self.piezas_encajadas_atras.sprites() + self.piezas_encajadas_adelante.sprites():
            self.robot.remove(p)
            p.fall()
            self.piezas.add(p)  
            self.dispatcher.stop()
  
        return self.father

def main():
    Level().loop()

if __name__ == "__main__py":
    main()
