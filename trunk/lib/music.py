import random
from config import *
import utils
import pygame
from pygame.locals import USEREVENT
import events
pygame.init()
pygame.mixer.init()

SOUNDS = {}
SOUNDS['explosion'] = utils.load_sound(EXPLOSION)
SOUNDS['peep'] = utils.load_sound(PEEP)
SOUNDS['alarm'] = utils.load_sound(ALARM)
SOUNDS['screw'] = utils.load_sound(SCREW)
SOUNDS['brokenThings'] = utils.load_sound(BROKENTHINGS)

last_music = None
playing = None

def play_explosion():
    SOUNDS['explosion'].play()

def play_screw():
    SOUNDS['screw'] = utils.load_soung(SCREW)

def play_brokenThings():
    SOUNDS['brokenThings'] = utils.load_soung(BROKENTHINGS)

def play_peep():
    SOUNDS['peep'].play(-1)
    
def stop_peep():
    SOUNDS['peep'].stop()
    
def play_alarm():
    SOUNDS['alarm'].play()

def play_countdown(times=0, start=0.0):
    SOUNDS['countdown'].play(loops=times)
    e = pygame.event.Event(events.INTRO, {})
    pygame.event.post(e)

def play_music(music_name, times=-1):
    global last_music
    global playing
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

def play_level(level):
    global playing
    music = MUSIC_LEVEL[level]
    play_music(music['loop'])
    #level_mus = pygame.mixer.Sound(music['loop'])
    #playing = level_mus
    #level_mus.play(-1)

#def stop_level():
    #global playing
    #playing.stop()

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def play_intro(level):
    music = MUSIC_LEVEL[level]
    a  = utils.load_sound(music['intro'])
    music_channel = pygame.mixer.Channel(0)
    music_channel.play(a)

    e = pygame.event.Event(events.INTRO, {})
    music_channel.set_endevent(88)
