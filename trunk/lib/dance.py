from visual import Visual
from config import *
import utils
import pygame
from pygame.locals import *

class HappyDance(object):
    def __init__(self, screen, menu):
        images = [utils.load_image(image) for image in DANCE_IMAGE]
        times = [0.05] * len(DANCE_IMAGE)
        
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((BLACK))
        step = 60
        font = pygame.font.Font(FONT_CREDITS, step)
        x = 335
        y = 30
        for line in HAPPY_DANCE_TEXT:
            img = font.render(line, True, WHITE)
            bg.blit(img, (x,y))
            y += step
        self.visual = Visual(screen, images, times, menu, loopear=False, pos=(0,210), bg=bg)

    def loop(self):
        while True:
            f = self.visual.loop()
            if f.teclaapretada:
                return f
            f = self.visual.loop(reverse=True)
            if f.teclaapretada:
                return f
