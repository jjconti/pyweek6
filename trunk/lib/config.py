import os
import glob
# configuraciones

# pantalla
WINDOW_TITLE = "Robot Factory"
WIDTH = 960
HEIGHT = 720
CENTER = HEIGHT / 2

CLOCK_TICS = 50

ROBOT_OFFSET = {1: (WIDTH / 2 - 265, HEIGHT / 2 - 340),
                2: (WIDTH / 2 - 265, HEIGHT / 2 - 340),
                3: (WIDTH / 2 - 265 + 27, HEIGHT / 2 - 340)}
MINI_ROBOT_OFFSET = (WIDTH - 170, 0)
#BACKGROUND_OFFSET = (270,20)
BAR_OFFSET = (WIDTH - 30, 220)

CINTA_LEN = 108

ALPHA_ROBOT = {1: 50,
               2: 50,
               3: 100}

# todos los path
DATA = os.path.join("data")
IMGS = os.path.join(DATA, "imgs")
FONTS = os.path.join(DATA, "fonts")
CREDITS = os.path.join(DATA, "credits.txt")
SOUNDS = os.path.join(DATA, "sounds")
BACKGROUND = os.path.join(IMGS, "background")
#STORY = os.path.join(DATA, "story.txt")

# tiempo que duran los niveles
TIME_LEVEL1 = 2200
TIME_LEVEL2 = 3100
TIME_LEVEL3 = 3600

# imagenes
LEVEL1 = os.path.join(IMGS, "level1")
LEVEL2 = os.path.join(IMGS, "level2")
LEVEL3 = os.path.join(IMGS, "level3")

#dance
DANCE_IMAGE = sorted(glob.glob('data/imgs/baile/*.png'))

PIECES_LEVEL = {1: os.path.join(LEVEL1, "pieces"),
                2: os.path.join(LEVEL2, "pieces"),
                3: os.path.join(LEVEL3, "pieces")}

ERRONEAS_LEVEL = {1: os.path.join(LEVEL1, "erroneas"),
                  2: os.path.join(LEVEL2, "erroneas"),
                  3: os.path.join(LEVEL3, "erroneas")}

GOLDEN_LEVEL =   {1: os.path.join(LEVEL1, "golden"),
                  2: os.path.join(LEVEL2, "golden"),
                  3: os.path.join(LEVEL3, "golden")}


FACES = os.path.join(IMGS, "faces")
DUDA, ENOJO, FELIZ, FELIZ2, FELIZ3, INCERTIDUMBRE, SORPRESA, MIEDO = range(1,9)
HISCORES = os.path.join(DATA, "scores.dat")
BACK = os.path.join(BACKGROUND, "opcion_de_menu.jpg")

HAND_AFTER_DRAG = os.path.join(IMGS, "hands/after_drag.png")
HAND_DRAG = os.path.join(IMGS, "hands/drag.png")

HELP = os.path.join(BACKGROUND, "help_inscription.png")

# Font
FONT_CREDITS = os.path.join(FONTS, "Retro 2.ttf")
#FONT_CREDITS = os.path.join(FONTS, "robot.ttf")

FONT_MENU = os.path.join(FONTS, "Retro 2.ttf") #de momento pongo esta hasta que encuentre alguna buena
FONTG = FONT_CREDITS 

#iconos para el menu
IMG_PLAY = os.path.join(IMGS, "menu/pedro.png")
IMG_STORY = os.path.join(IMGS, "menu/cesar_bn.png")
IMG_HELP = os.path.join(IMGS, "menu/juanjo.png")
IMG_DANCE = os.path.join(IMGS, "menu/guille.png")
IMG_SCORES = os.path.join(IMGS, "menu/gush.png")
IMG_CREDITS = os.path.join(IMGS, "menu/mariano.png")
IMG_EXIT = os.path.join(IMGS, "menu/humitos.png")

#colors
COLOR1 = (10, 50, 200) 
BLACK = (0, 0, 0)
GREEN = (0,250,0)
ORANGE = (255, 180, 0)
RED = (250, 0, 0)
WHITE = (250, 250, 250)
GREY = (100, 100, 100)
BLUE = (122, 138, 16)
YELLOW = (240, 255, 0)
CURRENT_COLOR = (0,185,0)
CELESTE_B0 = (82,115,136)
CELESTE_B0_SHADOW = (52,73,86)
CELESTE_B1 = (96,139,164)
CELESTE_B2 = (119,166,193)

INTRO = os.path.join(IMGS, "intro")
INTRO_IMAGES = sorted(glob.glob(INTRO+'/*.png'))
INTRO_XY = {'intro0001':(265,  50),'intro0003':(265,  51),'intro0005':(265,  51),'intro0007':(265,  51),'intro0009':(265,  51),
            'intro0011':(265,  51),'intro0013':(265,  51),'intro0015':(265,  51),'intro0017':(265,  51),'intro0019':(265,  51),
            'intro0021':(265,  51),'intro0023':(265,  72),'intro0025':(265,  72),'intro0027':(236,  72),'intro0029':(231,  94),
            'intro0031':(206, 122),'intro0033':(206, 187),'intro0035':(206, 237),'intro0037':(206, 322),'intro0039':(206, 356),
            'intro0041':(206, 349),'intro0043':(206, 356) }

LEVEL_IMAGES = sorted(glob.glob(IMGS+'/blueprint/*.png'))

INTRO_TIMES = [0.22] * len(INTRO_IMAGES)
#MISC = os.path.join(IMGS, "misc")
#MISC_IMAGES = sorted(glob.glob(MISC+'/*.png'))

#backgrounds
BACKINTRO_IMAGE = BACKGROUND+"/opcion de menu_fix.jpg"
BACKMENU_IMAGEN = BACKGROUND+"/opcion de menu_fix.jpg"
STORYBG = BACKGROUND+"/storybg.jpg"

BACKLEVEL1 = BACKGROUND+"/nivel1.jpg"
BACKLEVEL2 = BACKGROUND+"/nivel1.jpg"
BACKLEVEL3 = BACKGROUND+"/nivel3.jpg"

BACKLEVEL = {1: BACKLEVEL1, 2:BACKLEVEL2, 3:BACKLEVEL3}

#musicas
MENUMUSIC = os.path.join(SOUNDS, "menu.ogg")
BAILEMUSIC = os.path.join(SOUNDS, "el_martillo.ogg")
#musicas de los niveles
MUSIC_LEVEL = {1: {'intro': os.path.join(SOUNDS, "level1_intro.ogg"),
                   'loop': os.path.join(SOUNDS, "level1.ogg")},
               2: {'intro': os.path.join(SOUNDS, "level2_intro.ogg"),
                   'loop': os.path.join(SOUNDS, "level2.ogg")},
               3: {'intro': os.path.join(SOUNDS, "level3.ogg"),
                   'loop': os.path.join(SOUNDS, "level3_intro.ogg")}}

MUSIC_CREDITS = {'intro': os.path.join(SOUNDS, "credits_intro.ogg"),
                 'loop': os.path.join(SOUNDS, "credits_loop.ogg")}

#sonidos
EXPLOSION = os.path.join(SOUNDS, "Explode2.ogg")
PEEP = os.path.join(SOUNDS, "peep.ogg")
ALARM = os.path.join(SOUNDS, "alarm_beeps.ogg")
SCREW = os.path.join(SOUNDS, "screw.ogg")
BROKENTHINGS = os.path.join(SOUNDS, "brokenThings.ogg")
FART = os.path.join(SOUNDS, "fart.ogg")
FART2 = os.path.join(SOUNDS, "fart2.wav")
HAMMER = os.path.join(SOUNDS, "hammer.wav")

#backgrounds
HELPBG = os.path.join(BACKGROUND, "help.jpg")


IMAGE_CREDITS = (os.path.join(BACKGROUND, "1.jpg"), os.path.join(BACKGROUND, "2.jpg"), os.path.join(BACKGROUND, "3.jpg"))
IMAGE_GENERIC = (os.path.join(BACKGROUND, "1.jpg"), os.path.join(BACKGROUND, "2.jpg"), 
                 os.path.join(BACKGROUND, "3.jpg"), os.path.join(BACKGROUND, "4.jpg"), 
                 os.path.join(BACKGROUND, "5.jpg"), os.path.join(BACKGROUND, "6.jpg"))

HAPPY_DANCE_TEXT = [
"Thanks you for ",
"playing Robot Factory!",
"a game from the",
"authors of",
"Twisted Zombie",
"",
"Santa Fe",
"Argentina"]

STORY = [
'Pedro is a modest man.',
'One day, he read a book by Isaac Asimov',
'and began to dream about robots (Robot Dreams).',
'Time later, Pedro invest his money in a Robot Factory',
'called "Pedro\'s Robot Factory" (of course) and you',
'are his roboticist (Sorry).',
'Pedro developed the "Funnelhead" model',
'...and you must to build it.',
'Pedro is a demanding boss and level to level,',
'while the enterprise progress, you must be faster.',
'Enjoy!']

HELP = [
'Help Pepe to manufacture his',
'robots!',
'Right click to pick up/drop pieces.', 
'Scrol Up/Scroll Down or A/D key',
'to rotate the picked piece.',
'P key for pause.',
'Special pieces gives you',
'bonus points!']

THANKS = [
'Thanks:',
'',
'PyAr',
'PyWeek',
'',
'And of course thanks to the manufacters',
'of all the the mate, tea and',
'coffee we drank tonight.',
'',
'http://code.google.com/p/pyweek6/'
]

MESSAGE = [
'Sorry, you didn\'t win this game yet.',
'You have to complete the three levels first.']


