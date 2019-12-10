from player import *
from location import *


def setupIcons(all_sprites_list):
    pacman_collide = pygame.sprite.RenderPlain()

    Pacman = Player(w, p_h, "images/pacmanicon.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)