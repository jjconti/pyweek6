import sys
import pygame
from pygame.locals import *
from config import  *
from level import Level
#from menu import Menu
#from scores import HighScores
#from visual import Visual
#from help import Help
#from credits import Credits


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
    #images = [utils.load_image(image) for image in INTRO_IMAGES]
    #visual = Visual(screen, images, INTRO_TIMES)
    #music.play_music(INTROMUSIC, 1)
    #visual.loop()
    #music.stop_music()
    
    #Shooter opcion
    #opcion = menu
    #while opcion is not exit:
    #    change = opcion(screen).loop()
    #    if change:
    #        opcion = change
    #opcion()        #Exit

    level = Level(screen, None) 
    level.loop()

def exit():
    sys.exit(0)

if __name__ == "__main__":
    main()
