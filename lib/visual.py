import sys
import pygame
from pygame.locals import *
import glob
import utils

class Visual(object):
    def __init__(self, screen, images, times, func=None, loopear=False):
        self.screen = screen
        self.images = images
        if times == -1:
            self.times = -1
        else:
            self.times = [x*1000 for x in times]
        self.func = func    #father function
        self.loopear = loopear
        

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
                #si se le pone una imagen de fondo hay que sacar este
                #fill
                self.screen.fill((0,0,0))
                self.screen.blit(image, (0,0))
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
        if self.loopear:
            self.loop(reverse=True)
        return self.func

if __name__ == '__main__':
    print 'main'
    def prueba():
        print 'funcion devuelta'

    pygame.init()
    size = (700,550)
    screen = pygame.display.set_mode(size)
    fill = [(0,0,0), (255,255,255), (127,127,127), (50,50,50)]
    FINISH_IMAGE = sorted(glob.glob('/home/manuel/proyectos/pyweek6/data/imgs/intro/*.png'))
    images = [utils.load_image_alpha(image) for image in FINISH_IMAGE]
    times = [0.25] * len(FINISH_IMAGE)
    visual = Visual(screen, images, times, prueba, loopear=False)
    func = visual.loop()
    func()
