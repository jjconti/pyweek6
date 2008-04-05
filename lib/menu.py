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
        self.imagenes = []
        
        #cargamos las imagenes del menu
        nombres = [IMG_PLAY,IMG_STORY,IMG_HELP,IMG_DANCE,IMG_SCORES,IMG_CREDITS,IMG_EXIT]
        for nombre in nombres:
            self.imagenes.append(utils.load_image_alpha(nombre))

        #fuentes
        font1 = pygame.font.Font(FONT_MENU, 35)
        font2 = pygame.font.Font(FONT_MENU, 60)
        font_b1 = pygame.font.Font(FONT_MENU, 20)
        font_b2 = pygame.font.Font(FONT_MENU, 15)

        #separacion entre los items del menu
        self.hor_step = font2.get_height() - 15 
        
        self.clock = pygame.time.Clock()
        #fuentes de adelante
        self.selected_imgs = [font2.render(text, True, CURRENT_COLOR) for text in self.items]
        self.selected_imgs2 = [font2.render(text, True, BLACK) for text in self.items]
        self.unselected_imgs = [font1.render(text, True, CELESTE_B0) for text in self.items]
        self.unselected_imgs2 = [font1.render(text, True, CELESTE_B0_SHADOW) for text in self.items]
        
        #fuentes de atras
        self.unselected_imgs_b1 = [font_b1.render(text, True, CELESTE_B1) for text in self.items]
        self.unselected_imgs2_b1 = [font_b1.render(text, True, CELESTE_B1) for text in self.items]
        self.unselected_imgs_b2 = [font_b2.render(text, True, CELESTE_B2) for text in self.items]
        self.unselected_imgs2_b2 = [font_b2.render(text, True, CELESTE_B2) for text in self.items]
        
        self.unselected_rects = None
        self.timeloop = 0
        self.state = 0
        self.background = utils.load_image(BACKMENU_IMAGEN)
        title_img = font1.render(title, True, YELLOW)
        title_img2 = font1.render(title, True, RED)
        topleft = (self.background.get_rect().width - title_img.get_rect().width) / 2, 30
        topleft2 = (self.background.get_rect().width - title_img.get_rect().width) / 2-self.separator, 30-self.separator
        #self.background.blit(title_img2, topleft2)
        #self.background.blit(title_img, topleft)

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

            #if pygame.event.peek([KEYDOWN, KEYUP, QUIT]):
            for event in pygame.event.get():
                self.control(event)

            self._draw_items()
            pygame.display.flip()

            #self.timeloop += 1
            #if self.timeloop == 50:
            #    self.state=1
        #print "hola"
        self.draw_end = False
        '''while not self.done: # menu draw only if some key is pressed
            
            self.clock.tick(CLOCK_TICS)

            self.screen.blit(self.background, (0,0))

            pygame.event.clear()
            event = pygame.event.wait()
            self.control(event)

            self._draw_items()
            pygame.display.flip()

            self.timeloop += 1
            if self.timeloop == 50:
                self.state=1'''
        music.stop_music()
        return self.returns[self.index]

    def control(self, event):
        
        if event.type == QUIT:
            print 'hola mans'
            sys.exit(0)
        if event.type == KEYDOWN:
            if event.key in (K_SPACE, K_RETURN, K_KP_ENTER):
                #music.play_menu2()
                self.select()
            elif event.key in [K_LEFT]:
                #music.play_menu1()
                if self.index > 0:
                    self.set_index(self.index - 1)
                else:
                    self.set_index(self.last_index)
            elif event.key in [K_RIGHT]:
                #music.play_menu1()
                if self.index < self.last_index:
                    self.set_index(self.index + 1)
                else:
                    self.set_index(0)

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
        #rects = []
        # el valor de y es el mismo siempre
        y = self.hor_step + 470
        #separador = 150
        
        #dibuja la imagen
        indice = (self.index + 1) % len(self.items)
        img = self.unselected_imgs[indice]
        img2 = self.unselected_imgs2[indice]
        mitadIndex = ( img2.get_width() / 2 )
        x = (3 * WIDTH / 4) - mitadIndex
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        correc = 0
        if indice == 3:
            correc = -15
        if indice == 4:
            correc = 5
        if indice == 5:
            correc = 21
        if indice == 2:
            correc = 3
        if indice == 6:
            correc = -7
        print indice
        posicion =  ((WIDTH / 2) - self.imagenes[self.index].get_width()/2, y - 110 + correc)
        self.screen.blit(self.imagenes[self.index], posicion)
        
        #dibuja el item seleccionado en el medio
        x = (WIDTH / 2)
        img = self.selected_imgs[self.index]
        img2 = self.selected_imgs2[self.index]
        mitadIndex = ( img2.get_width() / 2 )
        x -= mitadIndex
        medioY = 100
        y += medioY
        self.screen.blit(img2, (x-self.separator,y-self.separator))
        self.screen.blit(img, (x,y))
        y -= medioY

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
        
        