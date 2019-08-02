from random import randint
from src.Player import Player
from src.Obstacle import TreeObstacle, BirdObstacle
from src.BackgroundObjects import Surface
import pygame
import queue
import time

windowWidth = 1200
windowHeight = 600
FPS = 60


class Game(object):

    def __init__(self):
        self.on_init()
        self.player = Player(windowHeight)
        self.player.rect.center = (70, windowHeight / 2)
        self.surface = Surface()
        self.surface.rect.center = (70, windowHeight / 2 + 50)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.surface)
        self.obstacles = queue.Queue()
        self.velocity = 8
        self.running, self.alive = True, True
        self.isJump = False

    def on_init(self):
        pygame.init()
        self.win = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
        self.win.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('T-Rex Game')

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

        elif key[pygame.K_DOWN]:
            self.player.crouch()

    def check_overlap(self):

        while self.obstacles.queue[0].rect.x + self.obstacles.queue[0].rect.w < self.player.rect.x:
            self.obstacles.get()
            if self.obstacles.empty():
                return

        if self.obstacles.empty():
            return

        obstacle = self.obstacles.queue[0]
        # Player and obstacle horizontally apart
        if self.player.rect.x - 5 > (obstacle.rect.x + obstacle.rect.w) or obstacle.rect.x > (self.player.rect.x - 5 + self.player.rect.w):
            return

        # Player and obstacle vertically apart
        if self.player.rect.y + 5 < (obstacle.rect.y - obstacle.rect.h) or obstacle.rect.y < (self.player.rect.y + 5 - self.player.rect.h):
            return

        self.alive = False

    def spawn_obstacles(self):

        if not self.obstacles.empty():
            if randint(1,60) != 60 or self.obstacles.queue[-1].rect.right + 450 > windowWidth:
                return
        else:
            if randint(1, 60) != 60:
                return

        if randint(1, 5) == 5:
            bird = BirdObstacle()
            bird.rect.center = (windowWidth, windowHeight / 2 - 200)
            self.all_sprites.add(bird)
            self.obstacles.put(bird)
        else:
            tree = TreeObstacle()
            tree.rect.center = (windowWidth, windowHeight / 2)
            self.all_sprites.add(tree)
            self.obstacles.put(tree)

    def death_recap(self):
        while self.running:
            self.clock.tick(FPS/2)

            for event in pygame.event.get():
                self.on_event(event)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break

        self.alive = True
        # Create new instance of a game
        self = Game()
        self.execute()

    def execute(self):
        ''' Main program loop
        '''

        while self.running and self.alive:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.on_event(event)

            self.check_key_pressed()

            # Update
            self.velocity += 0.001
            self.all_sprites.update(self.velocity)

            # If the ground has almost reached its end
            if self.surface.rect.x + self.surface.rect.w <= windowWidth:
                self.surface = Surface()
                self.surface.rect.center = (self.surface.rect.x + self.surface.rect.w - 10, windowHeight / 2 + 50)
                self.all_sprites.add(self.surface)

            if not self.obstacles.empty():
                # Check for obstacle collision
                self.check_overlap()

            self.spawn_obstacles()

            # Draw / Render
            self.win.fill((255,255,255))
            pygame.draw.line(self.win, (0, 255, 0), (self.player.rect.x, self.player.rect.y), (self.player.rect.x + self.player.rect.w, self.player.rect.y))
            self.all_sprites.draw(self.win)
            pygame.display.flip()

        if self.alive :
            pygame.quit()
        else:
            self.death_recap()