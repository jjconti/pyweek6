import os

# configuraciones

# pantalla
WINDOW_TITLE = "Ojalata!"
WIDTH = 780
HEIGHT = 560
CENTER = HEIGHT / 2

CLOCK_TICS = 100

# todos los path
DATA = os.path.join("data")
IMGS = os.path.join(DATA, "imgs")
FONTS = os.path.join(DATA, "fonts")
CREDITS = os.path.join(DATA, "credits.txt")
# imagenes
LEVEL1 = os.path.join(IMGS, "level1")
LEVEL2 = os.path.join(IMGS, "level2")
LEVEL3 = os.path.join(IMGS, "level3")
PIECES_LEVEL = {1: os.path.join(LEVEL1, "pieces"),
                2: os.path.join(LEVEL2, "pieces"),
                3: os.path.join(LEVEL3, "pieces")}
# Font
FONT_CREDIT = os.path.join(FONTS, "GALACTOS.ttf")

