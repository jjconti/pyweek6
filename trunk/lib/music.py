import random
from config import *
import utils
import pygame
from pygame.locals import USEREVENT
pygame.init()
pygame.mixer.init()

SOUNDS = {}
SOUNDS['explosion'] = utils.load_sound(EXPLOSION)
SOUNDS['peep'] = utils.load_sound(PEEP)
SOUNDS['alarm'] = utils.load_sound(ALARM)

last_music = None

def play_explosion():
    SOUNDS['explosion'].play()

def play_peep():
    SOUNDS['peep'].play(-1)
    
def stop_peep():
    SOUNDS['peep'].stop()
    
def play_alarm():
    SOUNDS['alarm'].play()

def play_countdown(times=0, start=0.0):
    SOUNDS['countdown'].play(loops=times)

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



def level(level, loop):
    # QUITAR CUANDO ESTE LA MUSICA DEL LEVEL 3
    if level == 3:
        return
    music = MUSIC_LEVEL[level]
    intro_mus = pygame.mixer.Sound(music['intro'])
    level_mus = pygame.mixer.Sound(music['loop'])

    pygame.mixer.set_reserved(1)
    music_channel = pygame.mixer.Channel(0)
    music_vol = 1.0

    #pygame.event.clear()
    if loop:
        music_channel.play(level_mus)
    else:
        music_channel.play(intro_mus)
        music_channel.set_endevent(USEREVENT)
        music_channel.set_volume(music_vol)
