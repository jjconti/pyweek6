import pygame
from pygame.locals import *
from math import exp
import sys
import utils
import music
from config import *

class Menu(object):
    '''A generic menu user interface. Allow both keyboard and mouse selection'''

    def __init__(self, screen, options, title, index=0):
        self.screen = screen
        self.items = [x[0] for x in options]
        self.returns = [x[1] for x in options]
        self.last_index = len(self.items) - 1
        self.index = index
        self.done = False
        self.separator = 2
        
        #fuentes
        font1 = pygame.font.Font(FONT_MENU, 40)
        font2 = pygame.font.Font(FONT_MENU, 50)
        font_b1 = pygame.font.Font(FONT_MENU, 20)
        font_b2 = pygame.font.Font(FONT_MENU, 15)

        #separacion entre los items del menu
        self.hor_step = font2.get_height() - 15 
        
        self.clock = pygame.time.Clock()
        #fuentes de adelante
        self.selected_imgs = [font2.render(text, True, RED) for text in self.items]
        self.selected_imgs2 = [font2.render(text, True, BLACK) for text in self.items]
        self.unselected_imgs = [font1.render(text, True, GREY) for text in self.items]
        self.unselected_imgs2 = [font1.render(text, True, BLACK) for text in self.items]
        
        #fuentes de atras
        self.unselected_imgs_b1 = [font_b1.render(text, True, GREY) for text in self.items]
        self.unselected_imgs2_b1 = [font_b1.render(text, True, BLACK) for text in self.items]
        self.unselected_imgs_b2 = [font_b2.render(text, True, GREY) for text in self.items]
        self.unselected_imgs2_b2 = [font_b2.render(text, True, BLACK) for text in self.items]
        
        self.unselected_rects = None
        self.timeloop = 0
        self.state = 0
        self.background = utils.load_image(BACKMENU_IMAGEN)
        title_img = font1.render(title, True, YELLOW)
        title_img2 = font1.render(title, True, RED)
        topleft = (self.background.get_rect().width - title_img.get_rect().width) / 2, 30
        topleft2 = (self.background.get_rect().width - title_img.get_rect().width) / 2-self.separator, 30-self.separator
        self.background.blit(title_img2, topleft2)
        self.background.blit(title_img, topleft)

        self.draw_end = False
        self._draw_items()

    def loop(self):
        '''Returns the asosiated object for the selected item'''
        pygame.event.clear()
        if not music.is_playing_music():
           music.play_music(MENUMUSIC)
        while (not self.draw_end) and (not self.done): # menu draw the first time

            self.clock.tick(CLOCK_TICS)

            self.screen.blit(self.background, (0,0))

            if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
                for event in pygame.event.get():
                    self.control(event)

            self._draw_items()
            pygame.display.flip()

            self.timeloop += 1
            if self.timeloop == 50:
                self.state=1
        self.draw_end = False
        while not self.done: # menu draw only if some key is pressed

            self.clock.tick(CLOCK_TICS)

            self.screen.blit(self.background, (0,0))

            pygame.event.clear()
            event = pygame.event.wait()
            self.control(event)

            self._draw_items()
            pygame.display.flip()

            self.timeloop += 1
            if self.timeloop == 50:
                self.state=1
        music.stop_music()
        return self.returns[self.index]

    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_SPACE, K_RETURN, K_KP_ENTER):
                #music.play_menu2()
                self.select()
            elif event.key == K_UP:
                #music.play_menu1()
                if self.index > 0:
                    self.set_index(self.index - 1)
                else:
                    self.set_index(self.last_index)
            elif event.key == K_DOWN:
                #music.play_menu1()
                if self.index < self.last_index:
                    self.set_index(self.index + 1)
                else:
                    self.set_index(0)
        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            for i in range(len(self.unselected_rects)):
                r = self.unselected_rects[i]
                if r.collidepoint(x,y):
                    self.set_index(i)
                    return
        if event.type == MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for i in range(len(self.unselected_rects)):
                r = self.unselected_rects[i]
                if r.collidepoint(x,y):
                    self.select()
                    return

    def set_index(self, index):
        if self.index != index:
            #self.sounds["snd1"].play()
            self.index = index

    def select(self):
        #self.sounds["snd2"].play()
        self.done = True

    def _draw_items_nuevo(self):
        """Nuevo efecto
        """
        pass

    def _draw_items(self):
        """Hace la magia de las apariciones de las imagenes.
        """

        
        rects = []
        # el valor de y es el mismo siempre
        y = self.hor_step + 320 
        separador = 150
        
        #dibuja el item seleccionado en el medio
        x = (WIDTH / 2)
        img = self.selected_imgs[self.index]
        img2 = self.selected_imgs2[self.index]
        mitadIndex = ( img2.get_width() / 2 )
        x -= mitadIndex
        medioY = 35
        y += medioY
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        y -= medioY
        
        #dibuja el item de la derecha
        indice = (self.index + 1) % len(self.items)
        img = self.unselected_imgs[indice]
        img2 = self.unselected_imgs2[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (3 * WIDTH / 4) - mitadIndex
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        #dibuja el item de la izquierda
        indice = (self.index - 1)
        img = self.unselected_imgs[indice]
        img2 = self.unselected_imgs2[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (WIDTH / 4) - mitadIndex
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        atrasY1 = 60
        atrasY2 = 95
        atrasX1 = 45
        atrasX2 = -50
        #dibuja el item de la izquierda atras 1 
        indice = (self.index - 2)
        img = self.unselected_imgs_b1[indice]
        img2 = self.unselected_imgs2_b1[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (WIDTH / 4) - mitadIndex - atrasX1
        y -= atrasY1
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        #dibuja el item de la derecha atras 1
        indice = (self.index + 2) % len(self.items)
        img = self.unselected_imgs_b1[indice]
        img2 = self.unselected_imgs2_b1[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (3 * WIDTH / 4) - mitadIndex + atrasX1
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        #dibuja el item de la izquierda atras 2
        indice = (self.index - 3)
        img = self.unselected_imgs_b2[indice]
        img2 = self.unselected_imgs2_b2[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (WIDTH / 4) - mitadIndex - atrasX2
        y += atrasY1
        y -= atrasY2
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        #dibuja el item de la derecha atras 2
        indice = (self.index + 3) % len(self.items)
        img = self.unselected_imgs_b2[indice]
        img2 = self.unselected_imgs2_b2[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (3 * WIDTH / 4) - mitadIndex + atrasX2
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        
        #hay q mostrar solo tres
        '''
        for i in range(3):#range(len(self.items)):
            
            #indice = i
            #if i == 1:
            #    indice = self.index + 1
            #elif i== 2:
            #    indice = self.index - 1
            #print indice 
            
            if i == self.index:
                img = self.selected_imgs[i]
                img2 = self.selected_imgs2[i]
            else:
                img = self.unselected_imgs[i]
                img2 = self.unselected_imgs2[i]
            
            
            
            x -= ( img2.get_width() / 2 )

            self.screen.blit(img2, (x-self.separator,y-self.separator))
            self.screen.blit(img, (x,y))

            if self.unselected_rects is None:
                rects += [img.get_rect().move(x,y)]

            separador = 150
            if i == 0:
                x = (WIDTH / 2) + ( img2.get_width() / 2 ) + separador
            else:
                x = (WIDTH / 2) - ( img2.get_width() / 2 ) - separador
            #pdb.set_trace()
            #y += self.hor_step
        '''

        if self.unselected_rects is None:
            self.unselected_rects = rects
