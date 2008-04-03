import os
import glob
# configuraciones

# pantalla
WINDOW_TITLE = "Ojalata!"
WIDTH = 960
HEIGHT = 720
CENTER = HEIGHT / 2

CLOCK_TICS = 100

ROBOT_OFFSET = (WIDTH / 2 - 265, HEIGHT / 2 - 340)
#BACKGROUND_OFFSET = (270,20)

# todos los path
DATA = os.path.join("data")
IMGS = os.path.join(DATA, "imgs")
FONTS = os.path.join(DATA, "fonts")
CREDITS = os.path.join(DATA, "credits.txt")
SOUNDS = os.path.join(DATA, "sounds")
BACKGROUND = os.path.join(IMGS, "background")

# imagenes
LEVEL1 = os.path.join(IMGS, "level1")
LEVEL2 = os.path.join(IMGS, "level2")
LEVEL3 = os.path.join(IMGS, "level3")

PIECES_LEVEL = {1: os.path.join(LEVEL1, "pieces"),
                2: os.path.join(LEVEL2, "pieces"),
                3: os.path.join(LEVEL3, "pieces")}

ERRONEAS_LEVEL = {1: os.path.join(LEVEL1, "erroneas"),
                  2: os.path.join(LEVEL2, "erroneas"),
                  3: os.path.join(LEVEL3, "erroneas")}

FACES = os.path.join(IMGS, "faces")
DUDA, ENOJO, FELIZ, FELIZ2, FELIZ3, INCERTIDUMBRE, SORPRESA, MIEDO = range(1,9)

BACK = os.path.join(BACKGROUND, "taller.jpg")

HAND_AFTER_DRAG = os.path.join(IMGS, "hands/after_drag.png")
HAND_DRAG = os.path.join(IMGS, "hands/drag.png")

IMAGE_CREDITS = os.path.join(BACKGROUND, "credits.png")
HELP = os.path.join(BACKGROUND, "help_inscription.png")

# Font
FONT_CREDIT = os.path.join(FONTS, "GALACTOS.ttf")
#FONT_MENU = os.path.join(FONTS, "VeraBd.ttf") #de momento pongo esta hasta que encuentre alguna buena
FONT_MENU = os.path.join(FONTS, "Borobots.ttf") #de momento pongo esta hasta que encuentre alguna buena
FONTG = FONT_CREDIT 

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
BACKINTRO_IMAGE = BACKGROUND+"/taller.jpg"
BACKMENU_IMAGEN = BACKGROUND+"/taller.jpg"
#BACKLEVEL_IMAGE = BACKGROUND+"/fondoAzul.png"
BACKLEVEL_IMAGE = BACKGROUND+"/nivel1.png"

#musicas
MENUMUSIC = os.path.join(SOUNDS, "menu.ogg")

#sonidos
EXPLOSION = os.path.join(SOUNDS, "Explode2.wav")
PEEP = os.path.join(SOUNDS, "peep.ogg")
ALARM = os.path.join(SOUNDS, "alarm_beeps.wav")

#backgrounds
HELPBG = os.path.join(BACKGROUND, "help.jpg")
