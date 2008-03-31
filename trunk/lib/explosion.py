#! /usr/bin/env python

#game.py - By Michael Burns (pymike93@gmail.com)
#Part of Asterpods 2
#Copyright (C), 2007



import pygame, os
from pygame.locals import *

from utils import *
#from sound import *

#def load_exp(file):
      #img = load_image(os.path.join("explosion-big", file))
      #img = pygame.transform.scale(img, (img.get_width()/1.5, img.get_height()/1.5))
      #return img

#def load_exp2(file):
      #img = load_image(os.path.join("explosion-small", file))
      #img = pygame.transform.scale(img, (img.get_width()/1.25, img.get_height()/1.25))
      #return img

def load_exp3(file):
      img = load_image_alpha(os.path.join("data/explosion-medium", file))
      img = pygame.transform.scale(img, (img.get_width()*1, img.get_height()*1))
      return img

#def load_exp4(file):
      #img = load_image(os.path.join("explosion-big", file))
      #img = pygame.transform.scale(img, (img.get_width()*8, img.get_height()*8))
      #return img

pygame.init()
pygame.display.set_caption("loading...")
pygame.display.set_mode((800, 600))
#bigexpimgs = [load_exp("exp1.png"),
            #load_exp("exp2.png"),
            #load_exp("exp3.png"),
            #load_exp("exp4.png"),
            #load_exp("exp5.png"),
            #load_exp("exp6.png"),
            #load_exp("exp7.png"),
            #load_exp("exp8.png"),
            #load_exp("exp9.png"),
            #load_exp("exp10.png"),
            #load_exp("exp11.png"),
            #load_exp("exp12.png"),
            #load_exp("exp13.png"),
            #load_exp("exp14.png"),
            #load_exp("exp15.png"),
            #load_exp("exp16.png"),
            #load_exp("exp17.png"),
            #load_exp("exp18.png"),
            #load_exp("exp19.png"),
            #load_exp("exp20.png"),
            #load_exp("exp21.png"),
            #load_exp("exp22.png"),
            #load_exp("exp23.png"),
            #load_exp("exp24.png"),
            #load_exp("exp25.png")]

mediumexpimgs = [load_exp3("exp1.png"),
               load_exp3("exp2.png"),
               load_exp3("exp3.png"),
               load_exp3("exp4.png"),
               load_exp3("exp5.png"),
               load_exp3("exp6.png"),
               load_exp3("exp7.png"),
               load_exp3("exp8.png")]

#smallexpimgs = [load_exp2("exp1.png"),
               #load_exp2("exp2.png"),
               #load_exp2("exp3.png"),
               #load_exp2("exp4.png"),
               #load_exp2("exp5.png"),
               #load_exp2("exp6.png"),
               #load_exp2("exp7.png"),
               #load_exp2("exp8.png"),
               #load_exp2("exp9.png"),
               #load_exp2("exp10.png"),
               #load_exp2("exp11.png"),
               #load_exp2("exp12.png"),
               #load_exp2("exp13.png"),
               #load_exp2("exp14.png"),
               #load_exp2("exp15.png")]

#massiveexpimgs = [load_exp4("exp1.png"),
            #load_exp4("exp2.png"),
            #load_exp4("exp3.png"),
            #load_exp4("exp4.png"),
            #load_exp4("exp5.png"),
            #load_exp4("exp6.png"),
            #load_exp4("exp7.png"),
            #load_exp4("exp8.png"),
            #load_exp4("exp9.png"),
            #load_exp4("exp10.png"),
            #load_exp4("exp11.png"),
            #load_exp4("exp12.png"),
            #load_exp4("exp13.png"),
            #load_exp4("exp14.png"),
            #load_exp4("exp15.png"),
            #load_exp4("exp16.png"),
            #load_exp4("exp17.png"),
            #load_exp4("exp18.png"),
            #load_exp4("exp19.png"),
            #load_exp4("exp20.png"),
            #load_exp4("exp21.png"),
            #load_exp4("exp22.png"),
            #load_exp4("exp23.png"),
            #load_exp4("exp24.png"),
            #load_exp4("exp25.png")]

#class Explosion(pygame.sprite.Sprite):

      #def __init__(self, pos):

            #pygame.sprite.Sprite.__init__(self, self.containers)
            #self.images = bigexpimgs
            #self.image = self.images[0]
            #self.rect = self.image.get_rect(center = pos)
            #self.life = 72
            #self.frame = 72
            #s = load_sound("Explode.wav")
            #s.play()


      #def update(self):
            #self.life -= 1
            #if self.life <= 0:
                  #self.kill()
            #self.frame -= 1
            #self.image = self.images[self.frame/3%len(self.images)]

#class ExplosionMassive(pygame.sprite.Sprite):

      #def __init__(self, pos):

            #pygame.sprite.Sprite.__init__(self, self.containers)
            #self.images = massiveexpimgs
            #self.image = self.images[0]
            #self.rect = self.image.get_rect(center = pos)
            #self.life = 100
            #self.frame = 100
            #s = load_sound("Explode.wav")
            #s.play()


      #def update(self):
            #self.life -= 1
            #if self.life <= 0:
                  #self.kill()
            #self.frame -= 1
            #self.image = self.images[self.frame/4%len(self.images)]

class ExplosionMedium(pygame.sprite.Sprite):

      def __init__(self, pos):

            pygame.sprite.Sprite.__init__(self, self.containers)
            self.images = mediumexpimgs
            self.image = self.images[0]
            self.rect = self.image.get_rect(center = pos)
            self.life = 24
            self.frame = 0
            #s = load_sound("Explode 2.wav")
            #s.play()

      def update(self):
            self.life -= 1
            if self.life <= 0:
                  self.kill()
            self.frame += 1
            self.image = self.images[self.frame/3%len(self.images)]


#class ExplosionSmall(pygame.sprite.Sprite):

      #def __init__(self, pos):

            #pygame.sprite.Sprite.__init__(self, self.containers)
            #self.images = smallexpimgs
            #self.image = self.images[0]
            #self.rect = self.image.get_rect(center = pos)
            #self.life = 30
            #self.frame = 0
            #s = load_sound("Explosion.wav")
            #s.play()

      #def update(self):
            #self.life -= 1
            #if self.life <= 0:
                  #self.kill()
            #self.frame += 1
            #self.image = self.images[self.frame/2%len(self.images)]
