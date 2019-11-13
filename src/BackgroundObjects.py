import pygame, random


class Ground(pygame.sprite.Sprite):
    """ Ground that user-controlled object and Trees stand on

        Attributes
        ------------
        image : pygame.Surface
             image of the object
        rect : rectangle
            area which object covers on game surface
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\ground.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        """ Code to be executed to update the Ground during each frame of the game

            Attributes
            ------------
            args : float
                number of pixel to move the object
        """
        self.rect.x -= args[0]


class Cloud(pygame.sprite.Sprite):
    """ Clouds on the game surface

        Attributes
        ------------
        image : pygame.Surface
             image of the object
        rect : rectangle
            area which object covers on game surface
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("..\\img\\cloud.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()

    def update(self, *args):
        """ Code to be executed to update the Cloud during each frame of the game

            Attributes
            ------------
            args : float
                number of pixel to move the object
        """
        self.rect.x -= args[0]
