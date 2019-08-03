import pygame
import random


class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass


class TreeObstacle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\tree" + str(random.randint(1,5))+ ".png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()


    def update(self, *args):
        self.rect.x -= args[0]


class BirdObstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("..\\img\\bird0.png").convert(), pygame.image.load("..\\img\\bird1.png").convert()]
        self.image = self.images[0]
        self.index = 0
        self.count = 0
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.count += 1
        if self.count % 5 == 0:
            self.index = self.index ^ 1
            self.image = self.images[self.index]
        self.rect.x -= args[0]