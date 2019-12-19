from Ghosts import *

pacman_collide = pygame.sprite.RenderPlain()


def setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde):
    pacman_collide = pygame.sprite.RenderPlain()

    Pacman = Player(w, p_h, "images/pacmanicon.png")
    monsta_list = pygame.sprite.RenderPlain()
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    return Pacman, monsta_list
