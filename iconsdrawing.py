from player import *
from location import *
from Ghosts import  *

def setupIcons(all_sprites_list):
    pacman_collide = pygame.sprite.RenderPlain()


    Pacman = Player(w, p_h, "images/pacmanicon.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    monsta_list = pygame.sprite.RenderPlain()
    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w - 30, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)