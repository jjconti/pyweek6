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
               3: 150}

# todos los path
DATA = os.path.join("data")
IMGS = os.path.join(DATA, "imgs")
FONTS = os.path.join(DATA, "fonts")
CREDITS = os.path.join(DATA, "credits.txt")
SOUNDS = os.path.join(DATA, "sounds")
BACKGROUND = os.path.join(IMGS, "background")

# tiempo que duran los niveles
TIME_LEVEL1 = 1800
TIME_LEVEL2 = 2500
TIME_LEVEL3 = 3000

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

IMAGE_CREDITS = os.path.join(BACKGROUND, "credits.png")
HELP = os.path.join(BACKGROUND, "help_inscription.png")

# Font
#FONT_CREDITS = os.path.join(FONTS, "GALACTOS.ttf")
FONT_CREDITS = os.path.join(FONTS, "Retro 2.ttf")
#FONT_CREDITS = os.path.join(FONTS, "robot.ttf")

#FONT_MENU = os.path.join(FONTS, "VeraBd.ttf") #de momento pongo esta hasta que encuentre alguna buena
FONT_MENU = os.path.join(FONTS, "Retro 2.ttf") #de momento pongo esta hasta que encuentre alguna buena
FONTG = FONT_CREDITS 

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
CELESTE_B1 = ()
CELESTE_B2 = ()

INTRO = os.path.join(IMGS, "intro")
INTRO_IMAGES = sorted(glob.glob(INTRO+'/*.png'))
INTRO_XY = {'intro0001':(265,  50),'intro0003':(265,  51),'intro0005':(265,  51),'intro0007':(265,  51),'intro0009':(265,  51),
            'intro0011':(265,  51),'intro0013':(265,  51),'intro0015':(265,  51),'intro0017':(265,  51),'intro0019':(265,  51),
            'intro0021':(265,  51),'intro0023':(265,  72),'intro0025':(265,  72),'intro0027':(236,  72),'intro0029':(231,  94),
            'intro0031':(206, 122),'intro0033':(206, 187),'intro0035':(206, 237),'intro0037':(206, 322),'intro0039':(206, 356),
            'intro0041':(206, 349),'intro0043':(206, 356) }

INTRO_TIMES = [0.22] * len(INTRO_IMAGES)
MISC = os.path.join(IMGS, "misc")
MISC_IMAGES = sorted(glob.glob(MISC+'/*.png'))

#backgrounds
BACKINTRO_IMAGE = BACKGROUND+"/opcion de menu_fix.jpg"
BACKMENU_IMAGEN = BACKGROUND+"/opcion de menu_fix.jpg"
#BACKLEVEL_IMAGE = BACKGROUND+"/fondoAzul.png"
STORYBG = BACKGROUND+"/storybg.jpg"
STORY = BACKGROUND+"/story.png"

BACKLEVEL1 = BACKGROUND+"/nivel1.jpg"
BACKLEVEL2 = BACKGROUND+"/nivel1.jpg"
BACKLEVEL3 = BACKGROUND+"/nivel1.jpg"

BACKLEVEL = {1: BACKLEVEL1, 2:BACKLEVEL2, 3:BACKLEVEL3}
CARTELBACKLEVEL1 = BACKGROUND+"/cartel_nivel1.jpg"
CARTELBACKLEVEL2 = BACKGROUND+"/cartel_nivel2.jpg"
CARTELBACKLEVEL3 = BACKGROUND+"/cartel_nivel3.jpg"
CARTELBACKLEVEL = {1: CARTELBACKLEVEL1, 2:CARTELBACKLEVEL2, 3:CARTELBACKLEVEL3}

#musicas
MENUMUSIC = os.path.join(SOUNDS, "menu.ogg")
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
EXPLOSION = os.path.join(SOUNDS, "Explode2.wav")
PEEP = os.path.join(SOUNDS, "peep.ogg")
ALARM = os.path.join(SOUNDS, "alarm_beeps.wav")
SCREW = os.path.join(SOUNDS, "screw.wav")
BROKENTHINGS = os.path.join(SOUNDS, "brokenThings.wav")
FART = os.path.join(SOUNDS, "fart.wav")
HAMMER = os.path.join(SOUNDS, "hammer.wav")

#backgrounds
HELPBG = os.path.join(BACKGROUND, "help.jpg")


BACK_HAPPY_DANCE_FALSE = os.path.join(BACKGROUND, "4.jpg")

IMAGE_CREDITS = (os.path.join(BACKGROUND, "1.jpg"),
        os.path.join(BACKGROUND, "2.jpg"),
        os.path.join(BACKGROUND, "3.jpg"))

BACK_HAPPY_DANCE_FALSE = os.path.join(BACKGROUND, "4_1.jpg")
HAPPY_DANCE_TEXT = [
"Thanks you for ",
"playing Robot Factory!",
"a game from the",
"authors of",
"Twisted Zombie",
"",
"Santa Fe",
"Argentina"]
