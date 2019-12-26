from Ghosts import *

pacman_collide = pygame.sprite.RenderPlain()


def setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde):
    pacman_collide = pygame.sprite.RenderPlain()

    Pacman = Player(w2, p1, "images/pacmanicon.png")
    Pacman2 = Player(w1, p1, "images/pacmangirl.jpg")
    monsta_list = pygame.sprite.RenderPlain()
    all_sprites_list.add(Pacman)
    all_sprites_list.add(Pacman2)
    pacman_collide.add(Pacman)
    pacman_collide.add(Pacman2)

    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    return Pacman, Pacman2, monsta_list
