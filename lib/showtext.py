#!/usr/bin/python
# -*- coding: utf-8
          
import sys
import random
from visual import Visual          
import pygame
from pygame.locals import *
import utils
from config import  *
import events

class ShowText(object):
    def __init__(self, screen, func, text, color, background, image = None, offset = 0, y = 40):
        self.func = func
        self.screen = screen
        self.background = background
        self.image = image
        self.y = y
        self.color = color
        
        step = 60
        bg = utils.load_image(background)
        self.screen.blit(bg, (0,0))
        if self.image:
            self.screen.blit(self.image, (0,0))
        font1 = pygame.font.Font(FONTG, 35)
        for linea in text:
            myText = font1.render(linea, True, self.color)
            self.screen.blit(myText, ((WIDTH / 2 - myText.get_rect().width / 2 + offset), self.y))
            self.y += step            
            pygame.display.flip()

    def loop(self, reverse=False):
        while True:
            for event in pygame.event.get():
                if self.control(event):
                    return self.func

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN and event.key in (K_ESCAPE, K_KP_ENTER):
            return True
        if event.type == events.NUEVO_TEXTO:
            self.numero_texto = (self.numero_texto + 1) % len(self.developers)
            self.textos.sprites()[self.numero_texto].alive()
            
if __name__ == '__main__':
    print 'main'
    def myTest():
        print 'exit'

    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    background = random.choice(IMAGE_GENERIC)
    story = ShowText(screen, myTest, HELPBG, STORY)
    func = story.loop()
    func()
    
