import pygame, random


class Ground(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\ground.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.x -= args[0]


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\cloud.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.x -= args[0]