import pygame
from config import *

class Indicator(pygame.sprite.Sprite):
    
    def __init__(self, w, h, fsize):
        pygame.sprite.Sprite.__init__(self)
        self.size = w,h
        self.fsize = fsize
        self.font = pygame.font.Font(None, fsize)
        #self.image = self._image()
        #self.rect = self.image.get_rect(50, 50)

    def update(self, points, bonus, explosion):
        self.image = self._image(points, bonus, explosion)
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,20)

    def _image(self, points, bonus, explosions):
        img = pygame.Surface(self.size)
        img.fill(BLACK)
        img.convert()
        img.set_alpha(100)
        points = self.font.render("Points: " + str(points), True, WHITE, BLACK)
        points.set_colorkey(BLACK)
        bonus = self.font.render("Bonus: " + str(bonus), True, WHITE, BLACK)
        bonus.set_colorkey(BLACK)
        explosions = self.font.render("Explosions: " + str(explosions), True, WHITE, BLACK) 
        explosions.set_colorkey(BLACK)
        img.blit(points, (5,5))
        img.blit(bonus, (5,self.fsize + 5))
        img.blit(explosions, (5,2*self.fsize + 5))
        return img


