import pygame


class Player(pygame.sprite.Sprite):
    ''' User-controlled object (dinosaur)

        Parameters
        ------------
        windowHeight : int
            height of game window in pixels

        Attributes
        ------------
        images : list {pygame.Surface}
            all possible images of an object
        image : pygame.Surface
            current image of the object
        mass : float
            mass of an object
        velocity : float
            velocity of an object (used for jumping)
        index : int
            index of current image from images
        last_update : int
            time of a last image change
        rect : rectangle
            area which object covers on game surface
        isJump : bool
            if the object is currently in the process of jumping
        isCrouch : bool
            if the object is currently in the process of crouching
    '''

    def __init__(self, windowHeight):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("..\\img\\player_run0.png").convert(), pygame.image.load("..\\img\\player_run1.png").convert(),
                       pygame.image.load("..\\img\\player1.png").convert(), pygame.image.load("..\\img\\player_crouch.png").convert()]
        self.image = self.images[0]
        self.velocity = 7
        self.mass = 2
        self.index = 0
        self.last_update = pygame.time.get_ticks()
        self.image.set_colorkey((255, 255, 255))
        self.windowHeight = windowHeight
        self.rect = self.image.get_rect()
        self.isJump, self.isCrouch = False, False

    def jump(self):
        ''' User initiated jump action '''
        self.isJump = True

    def crouch(self):
        ''' User initiated crouch action '''
        self.isCrouch = True

    def update(self, *args):
        ''' Code to be executed during each frame of the game'''

        if self.isJump:
            if self.velocity >= 0:
                F = (0.5 * self.mass * (self.velocity * self.velocity))
            else:
                F = -(0.5 * self.mass * (self.velocity * self.velocity))

            # Change position
            self.rect.y = self.rect.y - F

            # Change velocity
            self.velocity = self.velocity - 0.5

            # If ground is reached, reset variables.
            if self.rect.y >= 254:
                self.rect.y = 254
                self.isJump = False
                self.velocity = 7

        elif self.isCrouch:
            self.image = self.images[3]
            self.rect = self.image.get_rect()
            self.rect.center = (60, self.windowHeight / 2 + 15)
            self.isCrouch = False

        else:
            #change picture every 100 milliseconds
            now = pygame.time.get_ticks()
            if now - self.last_update > 100:
                self.index = self.index ^ 1
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = (70, self.windowHeight / 2)
                self.last_update = now
                return

    def draw_rect(self, window):
        xx = self.rect.x + 5
        yy = self.rect.y + 5
        hh = self.rect.h
        ww = self.rect.w
        pygame.draw.line(window, (0, 255, 0), (xx, yy), (xx + ww, yy))
        pygame.draw.line(window, (0, 255, 0), (xx + ww, yy), (xx + ww, yy + hh))
        pygame.draw.line(window, (0, 255, 0), (xx, yy), (xx, yy + hh))
        pygame.draw.line(window, (0, 255, 0), (xx, yy + hh), (xx + ww, yy + hh))

