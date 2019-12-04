import  pygame
from color import *

class Food(pygame.sprite.Sprite):


    def __init__(self, color, width, height):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()