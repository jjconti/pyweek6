#!/usr/bin/python
# -*- coding: utf-8

import os
import sys
import pygame
from pygame.locals import *
import random

from config import  *
from level import Level
from menu import Menu
#from scores import HighScores
from intro import Intro
#from help import Help
from credits import Credits
from showtext import ShowText
from dance import HappyDance

from config import *
import utils
from visual import Visual
import data

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
	
list_robot = []
for fullname in LEVEL_IMAGES:
    list_robot.append(utils.load_image_alpha(fullname, 255))
							
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
    opcion = menu
    while opcion is not exit:
        change = opcion(screen).loop()
        if change:
            opcion = change
    opcion()
	
def menu(screen):
    options = [("Play", play), ("Story", story), ("Help", help), ("Happy Dance", happy_dance), \
               ("High Scores", scores), ("Credits", credits), ("Exit",  exit)]
    return Menu(screen, options, WINDOW_TITLE)

def happy_dance(screen):
    if not os.path.exists('.youwon'):
        image = random.choice(list_robot)
        background = random.choice(IMAGE_GENERIC)
        return ShowText(screen, menu, MESSAGE, WHITE, background, image, 0, 240)
    return HappyDance(screen, menu)

def play(screen):
    return Level(screen, menu, 1, 0)

def scores(screen):
    return HighScores(screen,menu)

def help(screen):
    return ShowText(screen,menu,HELP,BLACK,HELPBG,None,35,200)

def credits(screen):
    return Credits(screen,menu)

def story(screen):
    image = random.choice(list_robot)
    background = random.choice(IMAGE_GENERIC)
    return ShowText(screen,menu,STORY,WHITE,background,image,0,40)

def exit():
    sys.exit(0)

if __name__ == "__main__":
    main()

