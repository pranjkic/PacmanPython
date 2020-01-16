from drawing import *
from iconsdrawing import *
from Ghosts import *
from location import *
from DeusExMachina import *
from bonus import *
import pygame
import time
import threading
import math
import socket

HOST = '192.168.0.12'  # The remote host
PORT = 50005  # The same port as used by the server
s = 0
player = -1
noConnection = True

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)
font1 = pygame.font.Font("freesansbold.ttf", 100)
clock = pygame.time.Clock()
clockMonsta = pygame.time.Clock()
screen = pygame.display.set_mode([606, 606])
extraLife = pygame.sprite.RenderPlain()
bonus = pygame.sprite.RenderPlain()
globalScore1 = 0
globalScore2 = 0
globalLives1 = 3
globalLives2 = 3
countPlay = 0
p_turn = 0
p_steps = 0
b_turn = 0
b_steps = 0
i_turn = 0
i_steps = 0
c_turn = 0
c_steps = 0
FPS = 17
FPS_monsta = 3

PacmanGlobal = 0

Blinky = Ghost(w, b_h, "images/Blinky.png")
Pinky = Ghost(w, m_h, "images/Pinky.png")
Inky = Ghost(i_w, m_h, "images/Inky.png")
Clyde = Ghost(c_w, m_h, "images/Clyde.png")


def monsta_movement():
    global p_turn
    global p_steps
    global b_turn
    global b_steps
    global i_turn
    global i_steps
    global c_turn
    global c_steps

    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_steps = 0
    c_turn = 0

    while True:
        clockMonsta.tick(FPS_monsta)
        returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        print("", end=" ")  # iz nekog razloga bez ovog print-a ne radi
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


text = ''


def coordRecv(s, text, wall_list, gate):
    while True:
        clock.tick(15)
        bin = s.recv(5)
        text += str(bin, 'utf-8')
        if bin:
            koord1 = text.split(' ')[0]
            koord2 = text.split(' ')[1]

            PacmanGlobal.changespeed(int(koord1), int(koord2))
            text = ''

        PacmanGlobal.update(wall_list, gate)


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


x = threading.Thread(target=monsta_movement, args=(), daemon=True)


def startAppSingle():
    global p_turn
    global p_steps
    global b_turn
    global b_steps
    global i_turn
    global i_steps
    global c_turn
    global c_steps
    global FPS_monsta
    global clock
    global clockMonsta
    global s
    global PacmanGlobal
    global player
    global globalLives1
    global globalLives2
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    wall_list = setupRoom(all_sprites_list)
    gate = setupGate(all_sprites_list)

    background = pygame.Surface(screen.get_size())
    startTime = float("inf")
    heartInactive = Heart(w, p_h2, "images/heartNotActive.jpg")
    heartActive = Heart(w, p_h2, "images/heart.jpg")
    deusEx = False
    deusExActive = False
    pacman_picked_deus_ex = False
    pacman2_picked_deus_ex = False

    cherry = Cherry(w, p_h, "images/cherry.jpg")
    all_sprites_list.add(cherry)
    bonus_not_picked = True
    pacman_picked_bonus = False
    pacman2_picked_bonus = False

    (Pacman, Pacman2, monsta_list) = setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde)

    if player == 1:
        PacmanGlobal = Pacman2
    elif player == 2:
        PacmanGlobal = Pacman

    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    global countPlay
    global globalScore1
    global globalScore2
    score = 0
    score2 = 0
    done = False
    clock = pygame.time.Clock()
    global text

    while done is False:

        clock.tick(FPS)

        if (score + score2) >= 75 and not (deusEx):
            all_sprites_list.add(heartInactive)
            startTime = time.time()
            deusEx = True

        if (time.time() - startTime) >= 2:
            all_sprites_list.remove(heartInactive)
            all_sprites_list.add(heartActive)
            extraLife.add(heartActive)
            deusExActive = True
            startTime = float("inf")

        bonus.add(cherry)

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

        if deusExActive:
            pacman_picked_deus_ex = pygame.sprite.spritecollide(Pacman, extraLife, True)
            pacman2_picked_deus_ex = pygame.sprite.spritecollide(Pacman2, extraLife, True)

        if pacman_picked_deus_ex and deusExActive:
            globalLives1 += 1

        if pacman2_picked_deus_ex and deusExActive:
            globalLives2 += 1

        pacman_picked_bonus = pygame.sprite.spritecollide(Pacman, bonus, True)
        pacman2_picked_bonus = pygame.sprite.spritecollide(Pacman2, bonus, True)

        if pacman_picked_bonus and bonus_not_picked:
            bonus_not_picked = False
            score += 50
            globalScore1 += 50
        elif pacman2_picked_bonus and bonus_not_picked:
            bonus_not_picked = False
            score2 += 50
            globalScore2 += 50

        blocks_hit_list = pygame.sprite.spritecollide(Pacman, food_list, True)
        blocks_hit_list2 = pygame.sprite.spritecollide(Pacman2, food_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            globalScore1 += 1
            score += 1

        if len(blocks_hit_list2) > 0:
            globalScore2 += 1
            score2 += 1

        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score1: " + str(globalScore1) + ", lives: " + str(int(globalLives1)), True, blue)
        text2 = font.render("Score2: " + str(globalScore2) + ", lives: " + str(int(globalLives2)), True, blue)
        screen.blit(text, [10, 10])
        screen.blit(text2, [335, 10])

        if (score + score2) >= 260:
            countPlay += 1
            if countPlay < 3:
                FPS_monsta = FPS_monsta
                newLevel("You go to the next level!", 260, all_sprites_list, food_list, food_list2, monsta_list,
                         pacman_collide, wall_list, gate)
            else:
                if globalScore1 > globalScore2:
                    globalScore1 = 0
                    globalScore2 = 0
                    b_turn = 0
                    b_steps = 0
                    c_turn = 0
                    c_steps = 0
                    i_steps = 0
                    i_turn = 0
                    p_turn = 0
                    p_steps = 0
                    Blinky.__init__(w, b_h, "images/Blinky.png")
                    Inky.__init__(i_w, m_h, "images/Inky.png")
                    Pinky.__init__(w, m_h, "images/Pinky.png")
                    Clyde.__init__(c_w, m_h, "images/Clyde.png")
                    FPS_monsta = 3
                    playGame("Pacman 1 is the winner!", 145, all_sprites_list, food_list, food_list2, monsta_list,
                             pacman_collide, wall_list, gate)
                if globalScore2 > globalScore1:
                    globalScore1 = 0
                    globalScore2 = 0
                    b_turn = 0
                    b_steps = 0
                    c_turn = 0
                    c_steps = 0
                    i_steps = 0
                    i_turn = 0
                    p_turn = 0
                    p_steps = 0
                    Blinky.__init__(w, b_h, "images/Blinky.png")
                    Inky.__init__(i_w, m_h, "images/Inky.png")
                    Pinky.__init__(w, m_h, "images/Pinky.png")
                    Clyde.__init__(c_w, m_h, "images/Clyde.png")
                    FPS_monsta = 3
                    playGame("Pacman 2 is the winner!", 145, all_sprites_list, food_list, food_list2, monsta_list,
                             pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
        '''monsta_hit_list = False'''
        if monsta_hit_list:
            globalLives1 -= 1
            p_turn = 0
            p_steps = 0
            b_turn = 0
            b_steps = 0
            i_turn = 0
            i_steps = 0
            c_turn = 0
            c_steps = 0
            Blinky.__init__(w, b_h, "images/Blinky.png")
            Inky.__init__(i_w, m_h, "images/Inky.png")
            Pinky.__init__(w, m_h, "images/Pinky.png")
            Clyde.__init__(c_w, m_h, "images/Clyde.png")
            Pacman.__init__(w2, p1, "images/pacmanman.jpg")
            Pacman2.__init__(w1, p1, "images/pacmangirl.jpg")

            if globalLives1 <= 0 and globalLives2 > 0:
                text = font.render("Score1: " + str(score) + "/210, lives: " + str(int(globalLives1)), True, blue)
                screen.blit(text, [10, 10])
                globalScore1 = 0
                globalScore2 = 0
                playGame("Game Over! Pacman 2 is the winner!", 80, all_sprites_list, food_list, food_list2,
                         monsta_list, pacman_collide, wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(Pacman2, monsta_list, False)
        '''monsta_hit_list = False'''
        if monsta_hit_list:
            globalLives2 -= 1
            p_turn = 0
            p_steps = 0
            b_turn = 0
            b_steps = 0
            i_turn = 0
            i_steps = 0
            c_turn = 0
            c_steps = 0
            Blinky.__init__(w, b_h, "images/Blinky.png")
            Inky.__init__(i_w, m_h, "images/Inky.png")
            Pinky.__init__(w, m_h, "images/Pinky.png")
            Clyde.__init__(c_w, m_h, "images/Clyde.png")
            Pacman.__init__(w2, p1, "images/pacmanman.jpg")
            Pacman2.__init__(w1, p1, "images/pacmangirl.jpg")

            if globalLives2 <= 0 and globalLives1 > 0:
                text2 = font.render("Score2: " + str(score2) + "/210, lives: " + str(int(globalLives2)), True,
                                    blue)
                screen.blit(text2, [335, 10])
                globalScore1 = 0
                globalScore2 = 0
                playGame("Game Over! Pacman 1 is the winner!", 80, all_sprites_list, food_list, food_list2,
                         monsta_list, pacman_collide, wall_list, gate)

        pygame.display.flip()


def startApp():
    global p_turn
    global p_steps
    global b_turn
    global b_steps
    global i_turn
    global i_steps
    global c_turn
    global c_steps
    global FPS_monsta
    global clock
    global clockMonsta
    global s
    global PacmanGlobal
    global player
    global globalLives1
    global globalLives2
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    wall_list = setupRoom(all_sprites_list)
    gate = setupGate(all_sprites_list)

    background = pygame.Surface(screen.get_size())
    startTime = float("inf")
    heartInactive = Heart(w, p_h2, "images/heartNotActive.jpg")
    heartActive = Heart(w, p_h2, "images/heart.jpg")
    deusEx = False
    deusExActive = False
    pacman_picked_deus_ex = False
    pacman2_picked_deus_ex = False

    cherry = Cherry(w, p_h, "images/cherry.jpg")
    all_sprites_list.add(cherry)
    bonus_not_picked = True
    pacman_picked_bonus = False
    pacman2_picked_bonus = False

    (Pacman, Pacman2, monsta_list) = setupIcons(all_sprites_list, Blinky, Pinky, Inky, Clyde)

    if player == 1:
        PacmanGlobal = Pacman2
    elif player == 2:
        PacmanGlobal = Pacman

    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    global countPlay
    global globalScore1
    global globalScore2
    score = 0
    score2 = 0
    done = False
    clock = pygame.time.Clock()
    global text

    if player == -1:
        bin = s.recv(1)
        player = int(str(bin, 'utf-8'))
        if player == 1:
            bin = s.recv(5)
            PacmanGlobal = Pacman2
            th = threading.Thread(target=coordRecv, args=(s, text, wall_list, gate), daemon=True)
            th.start()
            x.start()
        elif player == 2:
            bin = s.recv(5)
            PacmanGlobal = Pacman
            th = threading.Thread(target=coordRecv, args=(s, text, wall_list, gate), daemon=True)
            th.start()
            x.start()
    '''s.setblocking(0)
    s.settimeout(10)'''

    if player != -1:
        while done is False:

            clock.tick(FPS)

            if (score + score2) >= 75 and not (deusEx):
                all_sprites_list.add(heartInactive)
                startTime = time.time()
                deusEx = True

            if (time.time() - startTime) >= 2:
                all_sprites_list.remove(heartInactive)
                all_sprites_list.add(heartActive)
                extraLife.add(heartActive)
                deusExActive = True
                startTime = float("inf")

            bonus.add(cherry)

            if player == 1:
                # Pacman.update(wall_list, gate)
                # Pacman2.update(wall_list, gate)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    text = ''
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            Pacman.changespeed(-30, 0)
                            text = '-30 0'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_RIGHT:
                            Pacman.changespeed(30, 0)
                            text = '30 0 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_UP:
                            Pacman.changespeed(0, -30)
                            text = '0 -30'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_DOWN:
                            Pacman.changespeed(0, 30)
                            text = '0 30 '
                            s.sendall(text.encode('utf8'))
                            text = ''

                        if player == 1:
                            Pacman.update(wall_list, gate)
                        elif player == 2:
                            Pacman2.update(wall_list, gate)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            Pacman.changespeed(30, 0)
                            text = '30 0 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_RIGHT:
                            Pacman.changespeed(-30, 0)
                            text = '-30 0'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_UP:
                            Pacman.changespeed(0, 30)
                            text = '0 30 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_DOWN:
                            Pacman.changespeed(0, -30)
                            text = '0 -30'
                            s.sendall(text.encode('utf8'))
                            text = ''

                        if player == 1:
                            Pacman.update(wall_list, gate)
                        elif player == 2:
                            Pacman2.update(wall_list, gate)

                    '''bin = s.recv(1024)
                    text += str(bin, 'utf-8')
                    if bin:
                        koord1 = text.split(' ')[0]
                        koord2 = text.split(' ')[1]
                        print(str(int(koord1)) + ' ' + str(int(koord2)))

                        Pacman2.changespeed(int(koord1), int(koord2))
                        text = ''

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
                            Pacman2.changespeed(0, -30)'''
            elif player == 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    text = ''
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            Pacman2.changespeed(-30, 0)
                            text = '-30 0'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_RIGHT:
                            Pacman2.changespeed(30, 0)
                            text = '30 0 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_UP:
                            Pacman2.changespeed(0, -30)
                            text = '0 -30'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_DOWN:
                            Pacman2.changespeed(0, 30)
                            text = '0 30 '
                            s.sendall(text.encode('utf8'))
                            text = ''

                        if player == 1:
                            Pacman.update(wall_list, gate)
                        elif player == 2:
                            Pacman2.update(wall_list, gate)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            Pacman2.changespeed(30, 0)
                            text = '30 0 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_RIGHT:
                            Pacman2.changespeed(-30, 0)
                            text = '-30 0'
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_UP:
                            Pacman2.changespeed(0, 30)
                            text = '0 30 '
                            s.sendall(text.encode('utf8'))
                            text = ''
                        if event.key == pygame.K_DOWN:
                            Pacman2.changespeed(0, -30)
                            text = '0 -30'
                            s.sendall(text.encode('utf8'))
                            text = ''

                        if player == 1:
                            Pacman.update(wall_list, gate)
                        elif player == 2:
                            Pacman2.update(wall_list, gate)

            '''bin = s.recv(1024)
            text += str(bin, 'utf-8')
            if bin:
                koord1 = text.split(' ')[0]
                koord2 = text.split(' ')[1]
                print(str(int(koord1)) + ' ' + str(int(koord2)))

                Pacman2.changespeed(int(koord1), int(koord2))
                text = ''

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
                    Pacman2.changespeed(0, -30)'''

            if deusExActive:
                pacman_picked_deus_ex = pygame.sprite.spritecollide(Pacman, extraLife, True)
                pacman2_picked_deus_ex = pygame.sprite.spritecollide(Pacman2, extraLife, True)

            if pacman_picked_deus_ex and deusExActive:
                globalLives1 += 1

            if pacman2_picked_deus_ex and deusExActive:
                globalLives2 += 1

            pacman_picked_bonus = pygame.sprite.spritecollide(Pacman, bonus, True)
            pacman2_picked_bonus = pygame.sprite.spritecollide(Pacman2, bonus, True)

            if pacman_picked_bonus and bonus_not_picked:
                bonus_not_picked = False
                score += 50
                globalScore1 += 50
            elif pacman2_picked_bonus and bonus_not_picked:
                bonus_not_picked = False
                score2 += 50
                globalScore2 += 50

            blocks_hit_list = pygame.sprite.spritecollide(Pacman, food_list, True)
            blocks_hit_list2 = pygame.sprite.spritecollide(Pacman2, food_list, True)

            # Check the list of collisions.
            if len(blocks_hit_list) > 0:
                globalScore1 += 1
                score += 1

            if len(blocks_hit_list2) > 0:
                globalScore2 += 1
                score2 += 1

            screen.fill(black)

            wall_list.draw(screen)
            gate.draw(screen)
            all_sprites_list.draw(screen)
            monsta_list.draw(screen)

            text = font.render("Score1: " + str(globalScore1) + ", lives: " + str(int(globalLives1)), True, blue)
            text2 = font.render("Score2: " + str(globalScore2) + ", lives: " + str(int(globalLives2)), True, blue)
            screen.blit(text, [10, 10])
            screen.blit(text2, [335, 10])

            if (score + score2) >= 260:
                countPlay += 1
                if countPlay < 3:
                    FPS_monsta = FPS_monsta
                    newLevel("You go to the next level!", 260, all_sprites_list, food_list, food_list2, monsta_list,
                             pacman_collide, wall_list, gate)
                else:
                    if globalScore1 > globalScore2:
                        globalScore1 = 0
                        globalScore2 = 0
                        b_turn = 0
                        b_steps = 0
                        c_turn = 0
                        c_steps = 0
                        i_steps = 0
                        i_turn = 0
                        p_turn = 0
                        p_steps = 0
                        Blinky.__init__(w, b_h, "images/Blinky.png")
                        Inky.__init__(i_w, m_h, "images/Inky.png")
                        Pinky.__init__(w, m_h, "images/Pinky.png")
                        Clyde.__init__(c_w, m_h, "images/Clyde.png")
                        FPS_monsta = 3
                        playGame("Pacman 1 is the winner!", 145, all_sprites_list, food_list, food_list2, monsta_list,
                                 pacman_collide, wall_list, gate)
                    if globalScore2 > globalScore1:
                        globalScore1 = 0
                        globalScore2 = 0
                        b_turn = 0
                        b_steps = 0
                        c_turn = 0
                        c_steps = 0
                        i_steps = 0
                        i_turn = 0
                        p_turn = 0
                        p_steps = 0
                        Blinky.__init__(w, b_h, "images/Blinky.png")
                        Inky.__init__(i_w, m_h, "images/Inky.png")
                        Pinky.__init__(w, m_h, "images/Pinky.png")
                        Clyde.__init__(c_w, m_h, "images/Clyde.png")
                        FPS_monsta = 3
                        playGame("Pacman 2 is the winner!", 145, all_sprites_list, food_list, food_list2, monsta_list,
                                 pacman_collide, wall_list, gate)

            monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
            '''monsta_hit_list = False'''
            if monsta_hit_list:
                globalLives1 -= 1
                p_turn = 0
                p_steps = 0
                b_turn = 0
                b_steps = 0
                i_turn = 0
                i_steps = 0
                c_turn = 0
                c_steps = 0
                Blinky.__init__(w, b_h, "images/Blinky.png")
                Inky.__init__(i_w, m_h, "images/Inky.png")
                Pinky.__init__(w, m_h, "images/Pinky.png")
                Clyde.__init__(c_w, m_h, "images/Clyde.png")
                Pacman.__init__(w2, p1, "images/pacmanman.jpg")
                Pacman2.__init__(w1, p1, "images/pacmangirl.jpg")

                if player == 1:
                    PacmanGlobal = Pacman2
                elif player == 2:
                    PacmanGlobal = Pacman

                if globalLives1 <= 0 and globalLives2 > 0:
                    text = font.render("Score1: " + str(score) + "/210, lives: " + str(int(globalLives1)), True, blue)
                    screen.blit(text, [10, 10])
                    globalScore1 = 0
                    globalScore2 = 0
                    playGame("Game Over! Pacman 2 is the winner!", 80, all_sprites_list, food_list, food_list2,
                             monsta_list, pacman_collide, wall_list, gate)

            monsta_hit_list = pygame.sprite.spritecollide(Pacman2, monsta_list, False)
            '''monsta_hit_list = False'''
            if monsta_hit_list:
                globalLives2 -= 1
                p_turn = 0
                p_steps = 0
                b_turn = 0
                b_steps = 0
                i_turn = 0
                i_steps = 0
                c_turn = 0
                c_steps = 0
                Blinky.__init__(w, b_h, "images/Blinky.png")
                Inky.__init__(i_w, m_h, "images/Inky.png")
                Pinky.__init__(w, m_h, "images/Pinky.png")
                Clyde.__init__(c_w, m_h, "images/Clyde.png")
                Pacman.__init__(w2, p1, "images/pacmanman.jpg")
                Pacman2.__init__(w1, p1, "images/pacmangirl.jpg")

                if player == 1:
                    PacmanGlobal = Pacman2
                elif player == 2:
                    PacmanGlobal = Pacman

                if globalLives2 <= 0 and globalLives1 > 0:
                    text2 = font.render("Score2: " + str(score2) + "/210, lives: " + str(int(globalLives2)), True,
                                        blue)
                    screen.blit(text2, [335, 10])
                    globalScore1 = 0
                    globalScore2 = 0
                    playGame("Game Over! Pacman 1 is the winner!", 80, all_sprites_list, food_list, food_list2,
                             monsta_list, pacman_collide, wall_list, gate)

            pygame.display.flip()



def playGame(message, left, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate):
    global FPS
    global FPS_monsta
    global p_turn
    global p_steps
    global b_turn
    global b_steps
    global i_turn
    global i_steps
    global c_turn
    global c_steps
    global Blinky
    global Pinky
    global Inky
    global Clyde
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    if globalScore1 == 0 and globalScore2 == 0:
                        pygame.quit()
                    del all_sprites_list
                    del food_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    del food_list2
                    FPS = 17
                    p_turn = 0
                    p_steps = 0
                    b_turn = 0
                    b_steps = 0
                    i_turn = 0
                    i_steps = 0
                    c_turn = 0
                    c_steps = 0
                    Blinky.__init__(303 - 16, b_h, "images/Blinky.png")
                    Inky.__init__(i_w, m_h, "images/Inky.png")
                    Pinky.__init__(303 - 16, m_h, "images/Pinky.png")
                    Clyde.__init__(c_w, m_h, "images/Clyde.png")
                    startApp()

        w = pygame.Surface((500, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (50, 200))  # (0,0) are the top-left coordinates

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()


def newLevel(message, left, all_sprites_list, food_list, food_list2, monsta_list, pacman_collide, wall_list, gate):
    global FPS
    global FPS_monsta
    global p_turn
    global p_steps
    global b_turn
    global b_steps
    global i_turn
    global i_steps
    global c_turn
    global c_steps
    global Blinky
    global Pinky
    global Inky
    global Clyde
    global noConnection
    counter = 3
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        if counter < 0:
            #for event in pygame.event.get():
            #print(event)
            del all_sprites_list
            del food_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            del food_list2
            FPS = 15
            p_turn = 0
            p_steps = 0
            b_turn = 0
            b_steps = 0
            i_turn = 0
            i_steps = 0
            c_turn = 0
            c_steps = 0
            Blinky.__init__(303 - 16, b_h, "images/Blinky.png")
            Inky.__init__(i_w, m_h, "images/Inky.png")
            Pinky.__init__(303 - 16, m_h, "images/Pinky.png")
            Clyde.__init__(c_w, m_h, "images/Clyde.png")
            pygame.event.clear()

            if noConnection is True:
                startAppSingle()
            else:
                startApp()

        '''w = pygame.Surface((500, 200))  # the size of your rect
        w.set_alpha(0)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (50, 200))  # (0,0) are the top-left coordinates'''

        text1 = font1.render(str(counter), True, white)
        screen.blit(text1, [left, 233])

        pygame.display.flip()

        time.sleep(2)
        text1 = font1.render('', True, white)
        screen.blit(text1, [left, 233])
        counter = counter - 1


if __name__ == '__main__':
    pygame.init()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            noConnection = False
            startApp()
        except:
            noConnection = True
            x.start()
            startAppSingle()

    pygame.quit()
