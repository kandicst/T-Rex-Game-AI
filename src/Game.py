from pygame.locals import *
from random import randint
from src.Player import Player
import pygame
import time

windowWidth = 1200
windowHeight = 600
FPS = 20


class Game(object):

    def __init__(self):
        self.on_init()
        self.player = Player(windowHeight)
        self.player.rect.center = (50, windowHeight / 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.isJump = False

    def on_init(self):
        pygame.init()
        self.win = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
        self.win.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('T-Rex Game')
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self):
        pass

    def jump(self):
        self.player.rect.y -= 5

    def check_key_pressed(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            self.player.jump()

        if key[pygame.K_DOWN]:
            self.player.crouch()

    def execute(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.on_event(event)

            self.check_key_pressed()

            # Update
            self.all_sprites.update()

            # Draw / Render
            self.win.fill((255,255,255))
            print(self.player.rect.x, self.player.rect.y)
            pygame.draw.line(self.win, (0, 255, 0), (self.player.rect.x, self.player.rect.y), (self.player.rect.x + 500, self.player.rect.y))
            self.all_sprites.draw(self.win)
            pygame.display.flip()

    pygame.quit()