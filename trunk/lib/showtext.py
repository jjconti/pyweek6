#!/usr/bin/python
# -*- coding: utf-8
          
import sys
import random
from visual import Visual          
import pygame
from pygame.locals import *
import utils
from config import  *

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
        font1 = pygame.font.Font(FONTG, 35)
        for linea in text:
            myText = font1.render(linea, True, self.color)
            self.screen.blit(myText, ((WIDTH / 2 - myText.get_rect().width / 2 + offset), self.y))
            self.y += step            
            pygame.display.flip()

    def loop(self, reverse=False):
        while not self._verifyKey():
            pass
        return self.func

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
    
