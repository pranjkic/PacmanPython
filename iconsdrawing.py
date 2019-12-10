from player import *
from location import *
from Ghosts import  *

def setupIcons(all_sprites_list):
    pacman_collide = pygame.sprite.RenderPlain()


    Pacman = Player(w, p_h, "images/pacmanicon.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    monsta_list = pygame.sprite.RenderPlain()
    Blinky = Ghost(w - 30, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(w + 30, i_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(w, c_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)