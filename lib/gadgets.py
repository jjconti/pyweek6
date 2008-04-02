import pygame
from config import *

class Points(pygame.sprite.Sprite):
    
    def __init__(self, points):
        pygame.sprite.Sprite.__init__(self)
        self.points = points
        self.font = pygame.font.Font(FONTG, 30)
        self.image = self._image()
        #self.rect = self.image.get_rect(50, 50)

    def update(self, points):
        self.points = points
        self.image = self._image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,30)

    def _image(self):
        return self.font.render("Points: " + str(self.points) + " ", True, RED)

class LevelIndicator(pygame.sprite.Sprite):
    
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.level = level
        self.font = pygame.font.Font(FONTG, 30)
        self.image = self._image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,75)

    def _image(self):
        return self.font.render("Level " + str(self.level), True, RED)

