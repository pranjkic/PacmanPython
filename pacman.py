from drawing import *
from iconsdrawing import *
from Ghosts import *
from location import *
import pygame

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([606, 606])


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


def startApp():
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    wall_list = setupRoom(all_sprites_list)
    gate = setupGate(all_sprites_list)

    background = pygame.Surface(screen.get_size())

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

    (Pacman, Pacman2, monsta_list) = setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde)

    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    score = 0
    score2 = 0
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Pacman2.changespeed(-30, 0)
                if event.key == pygame.K_d:
                    Pacman2.changespeed(30, 0)
                if event.key == pygame.K_w:
                    Pacman2.changespeed(0, -30)
                if event.key == pygame.K_s:
                    Pacman2.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    Pacman2.changespeed(30, 0)
                if event.key == pygame.K_d:
                    Pacman2.changespeed(-30, 0)
                if event.key == pygame.K_w:
                    Pacman2.changespeed(0, 30)
                if event.key == pygame.K_s:
                    Pacman2.changespeed(0, -30)

        Pacman.update(wall_list, gate)
        Pacman2.update(wall_list, gate)

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

        blocks_hit_list = pygame.sprite.spritecollide(Pacman, food_list, True)
        blocks_hit_list2 = pygame.sprite.spritecollide(Pacman2, food_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        if len(blocks_hit_list2) > 0:
            score2 += len(blocks_hit_list2)

        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score1: " + str(score) + "/210, lives: " + str(int(Pacman.lives / 5)), True, blue)
        text2 = font.render("Score2: " + str(score2) + "/210, lives: " + str(int(Pacman2.lives / 5)), True, blue)
        screen.blit(text, [10, 10])
        screen.blit(text2, [335, 10])

        if (score+score2) >= 210:
            playGame("Congratulations, you won!", 145, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

        if monsta_hit_list:
            Pacman.lives -= 1
            Pacman.__init__(w, p_h, "images/pacmanicon.png")
            if Pacman.lives <= 0:
                playGame("Game Over", 210, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman2, monsta_list, False)
        if monsta_hit_list:
            Pacman2.lives -= 1
            Pacman2.__init__(w, p_h2, "images/pacmanicon.png")
            if Pacman2.lives <= 0:
                playGame("Game Over", 210, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate)

        pygame.display.flip()


def playGame(message, left, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del food_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    del food_list2

                    startApp()

        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    startApp()
    pygame.quit()
