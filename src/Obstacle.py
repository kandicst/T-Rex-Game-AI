import pygame
import random


class TreeObstacle(pygame.sprite.Sprite):
    ''' Tree-like obstacle

        Attributes
        ------------
        image : pygame.Surface
            image of the object
        rect : rectangle
            area which object covers on game surface
    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\tree" + str(random.randint(1,5))+ ".png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        ''' Code to be executed to update the Tree obstacle during each frame of the game'''
        self.rect.x -= args[0]


class BirdObstacle(pygame.sprite.Sprite):
    ''' Bird obstacle

        Attributes
        ------------
        images : list {pygame.Surface}
            all possible images of an object
        image : pygame.Surface
            current image of the object
        index : int
            index of current image from images
        count : int
            used for changing images evey n frames
        rect : rectangle
            area which object covers on game surface

    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("..\\img\\bird0.png").convert(), pygame.image.load("..\\img\\bird1.png").convert()]
        self.image = self.images[0]
        self.index = 0
        self.count = 0
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        ''' Code to be executed to update the Bird obstacle during each frame of the game'''
        self.count += 1
        if self.count % 5 == 0:
            self.index = self.index ^ 1
            self.image = self.images[self.index]
        self.rect.x -= args[0]