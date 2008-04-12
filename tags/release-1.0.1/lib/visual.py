import sys
import pygame
from pygame.locals import *
import glob
import utils

class Visual(object):
    def __init__(self, screen, images, times, func=None, loopear=False, pos=(0,0), bg=None):
        self.screen = screen
        self.bg = bg
        self.pos = pos
        self.images = images
        if times == -1:
            self.times = -1
        else:
            self.times = [x*1000 for x in times]
        self.func = func    #father function
        self.func.teclaapretada = False
        self.loopear = loopear
        

    def loop(self, reverse=False):
        if self.times == -1:
            self.screen.blit(self.images, self.pos)
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
                if self.bg:
                    self.screen.blit(self.bg, (0,0))
                else:
                    self.screen.fill(BLACK)
                self.screen.blit(image, self.pos)
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
                                self.func.teclaapretada = True  # ;-)
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
    FINISH_IMAGE = sorted(glob.glob('data/imgs/baile/*.png'))
    print FINISH_IMAGE
    images = [utils.load_image_alpha(image) for image in FINISH_IMAGE]
    times = [0.2] * len(FINISH_IMAGE)
    visual = Visual(screen, images, times, prueba, loopear=False)
    func = visual.loop()
    func()
