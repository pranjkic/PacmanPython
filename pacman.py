from drawing import *
from iconsdrawing import *
from Ghosts import *
from location import *
import pygame


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


def startApp():
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list = setupRoom(all_sprites_list)
    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    Blinky = Ghost(w - 30, b_h, "images/Blinky.png")
    Pinky = Ghost(w, m_h, "images/Pinky.png")
    Inky = Ghost(i_w, m_h, "images/Inky.png")
    Clyde = Ghost(c_w, m_h, "images/Clyde.png")

    (Pacman, monsta_list) = setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde)

    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    done = False
    FPS = 10
    clock = pygame.time.Clock()

    while done is False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -30)

        Pacman.update(wall_list, gate)

        returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)

        returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        Inky.update(wall_list, False)

        returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        Clyde.update(wall_list, False)

        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    startApp()
    pygame.quit()
