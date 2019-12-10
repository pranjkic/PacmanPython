import pygame
from drawing import *
import time
from iconsdrawing import *


def startApp():
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()
    setupIcons(all_sprites_list)
    wall_list = setupRoom(all_sprites_list)
    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    time.sleep(5)


if __name__ == '__main__':
    pygame.init()
    startApp()
    pygame.quit()