from drawing import *
from iconsdrawing import *


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


def startApp():
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pac-Man')
    all_sprites_list = pygame.sprite.RenderPlain()

    gate = setupGate(all_sprites_list)

    wall_list = setupRoom(all_sprites_list)
    (Pacman, monsta_list) = setupIcons(all_sprites_list)
    wall_list.draw(screen)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    done = False

    while done is False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-2, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(2, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, -2)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(2, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changespeed(-2, 0)
                if event.key == pygame.K_UP:
                    Pacman.changespeed(0, 2)
                if event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, -2)

        Pacman.update(wall_list, gate)

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
