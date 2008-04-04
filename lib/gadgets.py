import pygame
from config import *
import utils


class EnergyBar(pygame.sprite.Sprite):
    '''An energy bar'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.energy_percent = 100 #percent remanding of time
        self.image = self._image()
        self.rect = self.image.get_rect()
        self.rect.topleft = BAR_OFFSET

    def count(self):
        return max(0, self.energy_percent)

    def update(self, perc):
        self.energy_percent = 100 - perc
        self.image = self._image()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = BAR_OFFSET

    def _image(self):
        #font = pygame.font.Font(FONT1, 14)
        #text = font.render("Energy", True, BLACK)
        w = 15
        h = max(int(200 * self.energy_percent / 100), 0)

        if self.energy_percent > 60:
            color = GREEN
        elif self.energy_percent > 30:
            color = ORANGE
        else:
            color = RED
        img = utils.create_surface((w,h), color)
        #w1 = img.get_rect().width
        #w2 = text.get_rect().width
        #if w1 > 1.2 * w2:        
            #img.blit(text, (w1 - w2, 0))
        return img

class Hand(pygame.sprite.Sprite):
    '''An energy bar'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.catched = False
        self.image = self._image()
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self._image()
        self.rect.center   = pygame.mouse.get_pos()

    def _image(self):
        if self.catched:
            return utils.load_image_alpha(HAND_DRAG, -1)

        return utils.load_image_alpha(HAND_AFTER_DRAG, -1)

    def toggle(self):
        self.catched ^= True

    def select(self):
        self.catched = True

    def release(self):
        self.catched = False

    def collide(self, piece):
        return self.rect.colliderect(piece.rect)


class Indicator(pygame.sprite.Sprite):

    def __init__(self, w, h, fsize, level):
        pygame.sprite.Sprite.__init__(self)
        self.size = w,h
        self.fsize = fsize
        self.level = level
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
        level = self.font.render("Level: " + str(self.level), True, WHITE, BLACK)
        points = self.font.render("Points: " + str(points), True, WHITE, BLACK)
        points.set_colorkey(BLACK)
        bonus = self.font.render("Bonus: " + str(bonus), True, WHITE, BLACK)
        bonus.set_colorkey(BLACK)
        explosions = self.font.render("Explosions: " + str(explosions), True, WHITE, BLACK) 
        explosions.set_colorkey(BLACK)
        img.blit(level, (self.size[0] / 2 - level.get_rect().width / 2, 5))
        img.blit(points, (5,self.fsize + 5))
        img.blit(bonus, (5,2*self.fsize + 5))
        img.blit(explosions, (5,3*self.fsize + 5))
        return img


