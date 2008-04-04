from visual import Visual
from config import *
import utils

class HappyDance(object):
    def __init__(self, screen, menu):
        images = [utils.load_image_alpha(image) for image in DANCE_IMAGE]
        times = [0.1] * len(DANCE_IMAGE)
        self.visual = Visual(screen, images, times, None, loopear=False)
        #return visual
        #return menu

    def loop(self):
        self.visual.loop()