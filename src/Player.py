import pygame


class Player(pygame.sprite.Sprite):
    ''' Sprite for the player (dinosaur)

    '''

    v = 8
    m = 2

    def __init__(self, windowHeight):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("..\\img\\player_run0.png").convert(), pygame.image.load("..\\img\\player_run1.png").convert(),
                       pygame.image.load("..\\img\\player1.png").convert(), pygame.image.load("..\\img\\player_crouch.png").convert()]
        self.image = self.images[0]
        self.windowHeight = windowHeight
        self.index = 1
        self.rect = self.image.get_rect()
        self.isJump, self.isCrouch = False, False

    def jump(self):
        self.isJump = True

    def crouch(self):
        self.isCrouch = True

    def update(self, *args):

        if self.isJump:
            if self.v >= 0:
                F = (0.4 * self.m * (self.v * self.v))
            else:
                F = -(0.4 * self.m * (self.v * self.v))

            # Change position
            self.rect.y = self.rect.y - F

            # Change velocity
            self.v = self.v - 1

            # If ground is reached, reset variables.
            if self.rect.y >= 254:
                self.rect.y = 254
                self.isJump = False
                self.v = 8

        elif self.isCrouch:
            self.image = self.images[3]
            self.rect = self.image.get_rect()
            self.rect.center =  (60, self.windowHeight / 2 + 15)
            self.isCrouch = False

        else:
            self.index = self.index ^ 1
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (50, self.windowHeight / 2)
