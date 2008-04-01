import random
from config import *
import utils
import pygame
pygame.init()
pygame.mixer.init()

SOUNDS = {}
SOUNDS['explosion'] = utils.load_sound(EXPLOSION)
last_music = None

def play_explosion():
    SOUNDS['explosion'].play()

def play_music(music_name, times=-1):
    global last_music
    if last_music != music_name:
        last_music = music_name
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play(times)

def stop_music():
    global last_music
    last_music = None
    pygame.mixer.music.stop()

def is_playing_music():
    return last_music != None
