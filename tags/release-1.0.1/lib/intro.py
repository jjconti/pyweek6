import pygame
from pygame.locals import *
import sys
import os
import glob
import utils
from config import WIDTH, HEIGHT, INTRO, INTRO_XY, BACKINTRO_IMAGE
from music import play_screw, play_brokenThings, stop_brokenThings, play_hammer

ROBOT_OFFSET = (100, 80)

class Intro(object):
    def __init__(self, screen, func=None, loopear=False):
        self.screen = screen
        self.images = self.load_images()
        self.background = utils.load_image_alpha(BACKINTRO_IMAGE, -1)
        times = [0.1] * len(self.images)
        if times == -1:
            self.times = -1
        else:
            self.times = [x*1000 for x in times]
        self.func = func    #father function
        self.loopear = loopear

    def load_images(self):
        result = []
        for pathfile in sorted(glob.glob(os.path.join(INTRO, '*.png'))):
            myFile = os.path.basename(pathfile)
            myId = myFile[:-4]
            image = utils.load_image_alpha(pathfile, -1)
            result.append((myId, image))
        return result

    def loop(self, reverse=False):
        if self.times == -1:
            self.screen.blit(self.images, (0,0))
            pygame.display.flip()
            while True:
                pygame.event.clear()
                event = pygame.event.wait()
                if (event.type == QUIT):
                    sys.exit(0)
                elif (pygame.key.get_pressed()[K_RETURN]) or (pygame.key.get_pressed()[K_ESCAPE]):
                    pygame.event.clear()
                    break
            return self.func
        else:
            if reverse:
                self.images.reverse()
            for image, time_sleep in zip(self.images, self.times):
                #si se le pone una imagen de fondo hay que sacar este "fill"
                #self.screen.fill((0,0,0))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(image[1], (INTRO_XY[image[0]][0]+ROBOT_OFFSET[0], INTRO_XY[image[0]][1]+ROBOT_OFFSET[1]))
                if image[0] == 'intro0011':
                    play_screw()
                if image[0] == 'intro0025':
                    play_brokenThings()
                pygame.display.flip()
                i = 1
                while i < time_sleep:
                    pygame.time.delay(1)
                    i += 1
                    if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                sys.exit(0)
                            if event.type == KEYDOWN and \
                                (event.key in [K_ESCAPE, K_RETURN, K_KP_ENTER]):
                                return self.func
            pygame.time.delay(100)
            stop_brokenThings()
            pygame.time.delay(1000)

        if self.loopear:
            self.loop(reverse=True)
        return self.func

if __name__ == '__main__':
    print 'main'
    def prueba():
        print 'funcion devuelta'

    pygame.init()
    size = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(size)
    #fill = [(0,0,0), (255,255,255), (127,127,127), (50,50,50)]
    intro = Intro(screen, prueba, loopear=False)
    func = intro.loop()
    func()
    
