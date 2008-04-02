
import sys
import pygame
from pygame.locals import *
from config import  *
from level import Level
#from menu import Menu
#from scores import HighScores
from intro import Intro
#from help import Help
#from credits import Credits

from config import *
import utils

import data

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
	
							
def main():

    #Initialize 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    #icon = utils.load_image(ICON, (0,0,0))
    #pygame.display.set_icon(icon)

    #Introduction
    intro = Intro(screen, INTRO_TIMES)
    #music.play_music(INTROMUSIC, 1)
    intro.loop()
    
    #music.stop_music()
    
    #Shooter opcion
    #opcion = menu
    opcion = play
    while opcion is not exit:
        change = opcion(screen).loop()
        if change:
            opcion = change
    opcion()        #Exit

def play(screen):
    return Level(screen, None) 

def exit():
    sys.exit(0)

if __name__ == "__main__":
    main()

