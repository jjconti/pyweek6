from visual import Visual
from config import *
import utils

class HappyDance(object):
    def __init__(self, screen, menu):
        images = [utils.load_image_alpha(image) for image in DANCE_IMAGE]
        times = [0.05] * len(DANCE_IMAGE)
        self.visual = Visual(screen, images, times, menu, loopear=False)
        #return visual
        #return menu

    def loop(self):
        return self.visual.loop()
