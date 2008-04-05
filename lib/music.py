import random
from config import *
import utils
import pygame
from pygame.locals import USEREVENT
import events
pygame.init()
pygame.mixer.init()

# we have to reserve the first channel for the music of the levels
pygame.mixer.set_reserved(1)
music_channel = pygame.mixer.Channel(0)

# current loop to queue in the music_channel (this is to avoid the
# loading of the music each time it's looped)
music_current_loop = None

mus_e = pygame.event.Event(events.INTRO, {})
music_channel.set_endevent(events.INTRO)

SOUNDS = {}
SOUNDS['explosion'] = utils.load_sound(EXPLOSION)
SOUNDS['peep'] = utils.load_sound(PEEP)
SOUNDS['alarm'] = utils.load_sound(ALARM)
SOUNDS['screw'] = utils.load_sound(SCREW)
SOUNDS['brokenThings'] = utils.load_sound(BROKENTHINGS)
SOUNDS['fart'] = utils.load_sound(FART)
SOUNDS['fart2'] = utils.load_sound(FART2)
SOUNDS['hammer'] = utils.load_sound(HAMMER)

def play_explosion():
    SOUNDS['explosion'].play()

def play_screw():
    SOUNDS['screw'].play()

def play_hammer():
    SOUNDS['hammer'].play()

def play_brokenThings():
    SOUNDS['brokenThings'].play()

def stop_brokenThings():
    SOUNDS['brokenThings'].stop()

def play_peep():
    SOUNDS['peep'].play(-1)

def play_fart():
    fart = random.choice([SOUNDS['fart'], SOUNDS['fart2']])
    fart.play()
    
def stop_peep():
    SOUNDS['peep'].stop()

def play_alarm():
    SOUNDS['alarm'].play()

def play_countdown(times=0, start=0.0):
    SOUNDS['countdown'].play(loops=times)

def play_music(music_name, times=-1):
    stop_music()
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play(times)

def stop_music():
    global music_channel
    global music_current_loop

    pygame.mixer.music.stop()

    music_channel.stop()
    music_current_loop = None

def pause_music():
    global music_channel
    pygame.mixer.music.pause()
    music_channel.pause()

def unpause_music():
    global music_channel
    pygame.mixer.music.unpause()
    music_channel.unpause()

def play_intro(music):
    global music_channel
    global music_current_loop

    stop_music()

    intro = utils.load_sound(music['intro'])
    music_current_loop = utils.load_sound(music['loop'])
    music_channel.play(intro)
    music_channel.queue(music_current_loop)

def play_loop(music):
    global music_channel
    global music_current_loop

    music_channel.queue(music_current_loop)
