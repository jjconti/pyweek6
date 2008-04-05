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
import math
import music

from pieces import Pieces
from dispatcher import DispatcherCredit
##
# Módulos propios
from config import *
import events


class Texto(pygame.sprite.Sprite):
    def __init__(self, lista_imagenes):
        pygame.sprite.Sprite.__init__(self)

        self.lista_imagenes = lista_imagenes
        self.life = 0
        self.mod = round(self.life / len(self.lista_imagenes))
        self.image = self.lista_imagenes[0]
        self.rect = self.image.get_rect()
        self.rect.left = (WIDTH / 2 - self.image.get_width() / 2)


    def update(self):
        self.life -= 1
        
        if self.life in range(20, 30):
            return
        elif self.life > 0:
            self.image = self._image()
            self.rect.left = (WIDTH / 2 - self.image.get_width() / 2)
            #import pdb
            #pdb.set_trace()
        elif self.life == 0:
            e = pygame.event.Event(events.NUEVO_TEXTO, {})
            pygame.event.post(e)
        else:
            pass

    def _image(self):
        if not self.life % 5:
            self.proxima_imagen += 1
            self.rect.top += self.image.get_height()- (50 * .25)

        return self.lista_imagenes[self.proxima_imagen]
        
    def alive(self):
        self.rect.top = (WIDTH / 2) - 250 
        self.life = 75
        self.proxima_imagen = 0

class Credits(object):
    def __init__(self, screen, father=None):
        self.screen = screen
        self.father = father
        self.developers = []
        self.font = []
        self.font = self.generar_fuentes()
        self.level = 1

        self._load_credits()

        self.piezas = pygame.sprite.RenderUpdates()
        self.cargar_piezas()
        self.golden_piezas_used = pygame.sprite.RenderUpdates()
        self.golden_piezas = pygame.sprite.RenderUpdates()
        self.cargar_golden_piezas()
        self.piezas_erroneas = pygame.sprite.RenderUpdates()
        self.cargar_piezas_erroneas()

        self.textos = pygame.sprite.OrderedUpdates()
        self.cargar_textos()

        self.numero_texto = 0
        self.textos.sprites()[0].alive()

        self.clock = pygame.time.Clock()
        e = pygame.event.Event(events.END_INTRO, {})
        pygame.mixer.music.set_endevent(events.END_INTRO)
        music.play_music(MUSIC_CREDITS['intro'], 1)

        self.credit_dispatcher = DispatcherCredit(self.piezas, self.golden_piezas, self.piezas_erroneas)

    def generar_fuentes(self):
        """Crea la lista de tamaños de fuentes y la fuente en sí"""
        #base = 10
        sizes = [x for x in xrange(1, 35)]
        # Probando los sizes
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

    def loop(self):

        pygame.display.set_caption(WINDOW_TITLE)
        image = random.choice(IMAGE_CREDITS)
        self.background = pygame.image.load(image)
        """
        title = 'CREDITS'
        title_img = self.font[10].render(title, True, WHITE)
        topleft = (self.background.get_rect().width - title_img.get_rect().width) / 2, 30
        self.background.blit(title_img, topleft)
        """

        # Probemos con dos nomas
        lista_aux = self.developers
        while True:
            self.credit_dispatcher.dispatch()
            for event in pygame.event.get():
                if self.control(event):
                    return self.father
            self.update()
            self.draw()
            self.clock.tick(100)
            pygame.display.flip()

    def _load_credits(self):
        """Carga el archivo credits.txt. Con los nombres hace un shuffle para
        que cada vez que se muestre esta seccion sea distinto el orden de
        aparición."""
        try:
            credits = csv.reader(open(STORY))
            lista_nombre = []
            for pos, credit in enumerate(credits):
                if 0 < pos < 8 and len(credit) == 2:
                    lista_nombre.append(credit)
                elif pos == 8:
                    random.shuffle(lista_nombre)
                    for gente in lista_nombre:
                        self.developers.append(gente)
                    self.developers.append(credit)
                else:
                    self.developers.append(credit)
        except IOError:
            print 'Cannot open credits file'

    def _generar_imagenes(self, developer):
        """Genero por cada tamaño de letra una cantidad de palabras para ir
        mostrandolas en el mismo tiempo en distintas coordenadas"""
        lista = []
        for font in self.font:
            lista.append(font.render(developer, True, WHITE))
        return lista

    def update(self):
        self.piezas.update()
        self.piezas_erroneas.update()
        self.golden_piezas.update()
        #Probando credits
        title = 'CREDITS'
        title_img = self.font[10].render(title, True, WHITE)
        topleft = (self.background.get_rect().width - title_img.get_rect().width) / 2, 30
        self.background.blit(title_img, topleft)

        self.textos.update()


    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.piezas.draw(self.screen)
        self.piezas_erroneas.draw(self.screen)
        self.golden_piezas.draw(self.screen)
        self.textos.draw(self.screen)

    def _developers(self):
        print self.developers

    def _verifyKey(self):
        if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return self.father
                if event.type == KEYDOWN and \
                    (event.key in [K_ESCAPE, K_RETURN, K_KP_ENTER]):
                    return True
        return False

    def control(self, event):
        if event.type == KEYDOWN and event.key in (K_ESCAPE, K_KP_ENTER):
            music.stop_music()
            return True
            #sys.exit(0)
        if event.type == events.NUEVO_TEXTO:
            self.numero_texto = (self.numero_texto + 1) % len(self.developers)
            self.textos.sprites()[self.numero_texto].alive()

        if event.type == events.END_INTRO:
            music.play_music(MUSIC_CREDITS['loop'])

    def cargar_piezas(self):
        '''Cargar las imágenes y las posiciones en las que se tiene que dibujar.'''
        sets = [Pieces(type_piece="credit", level=self.level) for x in range(1)]
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
        sets = [Pieces(type_piece="erronea_credit", level=self.level) for x in
                range(4)]
        sprites = []
        for s in sets:
            sprites += s.get_all()
        self.piezas_erroneas.add(sprites)

    def cargar_textos(self):
        for text in self.developers:
            lista_imagenes = self._generar_imagenes(' '.join(text))
            self.textos.add(Texto(lista_imagenes))

if __name__ == '__main__':
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    credits = Credits(screen)
    credits.loop()
