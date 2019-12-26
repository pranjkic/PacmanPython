import pygame


class Heart(pygame.sprite.Sprite):

    def __init__(self, x, y, filename):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(filename).convert()

        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
