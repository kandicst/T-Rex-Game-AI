from random import randint
from src.Player import Player
from src.Obstacle import TreeObstacle, BirdObstacle
from src.BackgroundObjects import Ground, Cloud
import pygame
import queue
import math

windowWidth = 1280
windowHeight = 720
FPS = 60


class Game(object):
    '''
        Attributes
        ------------
        win : pygame.Surface
            game window
        clock : pygame.
            clocked used to keep up with the frame rate
        player : Player
            user-controlled object (Dinosaur)
        ground : Ground
            ground on the window
        all_sprites : list {pygame.sprite.Sprite}
            list of all objects to be updated during game run-time
        obstacles : queue {Obstacles}
            queue of all Obstacles on screen
        velocity : float
            how many pixel objects move each frame
        score : int
            game score
        cnt : int
            counter used to add up score attribute
        running :
            if the game is running
        alive : bool
            if the player is currently alive
        '''

    def __init__(self):
        self.win = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
        self.clock = pygame.time.Clock()
        self.player = Player(windowHeight)
        self.ground = Ground()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = queue.Queue()
        self.velocity = 8
        self.score = 0
        self.cnt = 0
        self.running, self.alive = True, True
        self.on_init()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('T-Rex Game')
        self.win.fill((255, 255, 255))
        self.player.rect.center = (70, windowHeight / 2)
        self.ground.rect.center = (70, windowHeight / 2 + self.ground.rect.h)
        self.all_sprites.add(self.player, self.ground)

    def on_event(self, event):
        ''' Handles specific pygame events '''

        if event.type == pygame.QUIT:
            self.running = False

    def check_key_pressed(self):
        ''' Gets all pressed keys in this frame
            and initiates needed actions
        '''

        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            self.player.jump()

        elif key[pygame.K_DOWN]:
            self.player.crouch()

    def show_score(self):
        ''' Shows the score of the current run'''
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, 22)
        text_surface = font.render('Score: ' + str(self.score), True, (0,0,0))
        text_rec = text_surface.get_rect()
        text_rec.topright = (windowWidth - 40, 30)
        self.win.blit(text_surface, text_rec)

        text_surface = font.render('Speed: ' + str(int(self.velocity)), True, (0, 0, 0))
        text_rec = text_surface.get_rect()
        text_rec.topright = (windowWidth - 40, 60)
        self.win.blit(text_surface, text_rec)


    def check_collision(self):
        ''' Checks if there was a collision
            between a player and the first obstacle
        '''

        while self.obstacles.queue[0].rect.x + self.obstacles.queue[0].rect.w < self.player.rect.x:
            self.obstacles.get()
            if self.obstacles.empty():
                return

        if self.obstacles.empty():
            return

        obstacle = self.obstacles.queue[0]
        # Player and obstacle horizontally apart
        if self.player.rect.x + 5 > (obstacle.rect.x + obstacle.rect.w) or obstacle.rect.x > (self.player.rect.x + 5 + self.player.rect.w - 5):
            return

        # Player and obstacle vertically apart
        if self.player.rect.y + 5 < (obstacle.rect.y - obstacle.rect.h) or obstacle.rect.y < (self.player.rect.y + 5 - (self.player.rect.h - 5)):
            return

        self.alive = False

    def activation_function(self):
        ''' Using the velocity, last added obstacle as well as random chance
            decides whether new obstacle should be created

            Returns
            ------------
            True if an obstacle should be created, False otherwise
        '''
        if not self.obstacles.empty():
            if randint(1, 60) == 60 or self.obstacles.queue[-1].rect.right + 750 > windowWidth:
                return False
        else:
            if randint(1, 60) == 60:
                return False

        return True

    def spawn_obstacles(self):
        ''' Randomly spawn objects on the game window '''

        # Approx every 3 seconds spawn a cloud
        if randint(1,180) == 180:
            cloud = Cloud()
            cloud.rect.center = (windowWidth, windowHeight / 2 - randint(180,250))
            self.all_sprites.add(cloud)

        if not self.activation_function():
            return

        # 20% chance of an obstacle being bird and 80% tree
        if randint(1, 5) == 5:
            bird = BirdObstacle()
            arr = [windowHeight / 2 , windowHeight / 2 - 70]    # low and high bird
            bird.rect.center = (windowWidth, arr[randint(0,1)])
            self.all_sprites.add(bird)
            self.obstacles.put(bird)
        else:
            tree = TreeObstacle()
            tree.rect.center = (windowWidth, windowHeight / 2)
            self.all_sprites.add(tree)
            self.obstacles.put(tree)

    def death_recap(self):
        ''' Game over scene :( '''

        repeat = pygame.image.load('..\\img\\repeat.png')
        game_over = pygame.image.load('..\\img\\game_over.png')

        while self.running:
            self.clock.tick(FPS/2)

            self.win.blit(game_over, (windowWidth/2 - game_over.get_width()/2, windowHeight / 2 - 80))
            self.win.blit(repeat, (windowWidth/2 - repeat.get_width()/2, windowHeight / 2 - 30))
            pygame.display.update()

            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                else:
                    self.on_event(event)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or clicked:
                break

        # If user clicked to exit the game
        if not self.running:
            exit()

        # If he clicked anywhere else just restart the game
        self.alive = True
        # Create new instance of a game
        self = Game()
        self.execute()

    def execute(self):
        ''' Main program loop '''

        while self.running and self.alive:
            self.clock.tick(60)

            for event in pygame.event.get():
                self.on_event(event)

            self.check_key_pressed()

            # Update
            self.velocity += 0.005
            self.cnt += 1
            # Score gradually increases by 10 pts every second
            if self.cnt % 6 == 0:
                self.score += 1
            self.all_sprites.update(self.velocity, self.win)

            # If the ground has almost reached its end
            if self.ground.rect.x + self.ground.rect.w <= windowWidth:
                self.ground = Ground()
                self.ground.rect.center = (self.ground.rect.x + self.ground.rect.w - 10, windowHeight / 2 + self.ground.rect.h)
                self.all_sprites.add(self.ground)

            if not self.obstacles.empty():
                # Check for obstacle collision
                self.check_collision()

            self.spawn_obstacles()

            # Draw / Render
            self.win.fill((255,255,255))
            self.show_score()
            #pygame.draw.line(self.win, (0, 255, 0), (200,300), (650 , 300))
            self.all_sprites.draw(self.win)
            pygame.display.flip()

        if self.alive :
            exit()
        else:
            self.death_recap()


    def draw_lines(self):
        ''' TODO DELETE AFTER'''
        xx = self.player.rect.x + 5
        yy = self.player.rect.y + 5
        hh = self.player.rect.h - 5
        ww = self.player.rect.w - 5
        pygame.draw.line(self.win, (0, 255, 0), (xx, yy), (xx + ww, yy))
        pygame.draw.line(self.win, (0, 255, 0), (xx + ww, yy), (xx + ww, yy + hh))
        pygame.draw.line(self.win, (0, 255, 0), (xx, yy), (xx, yy + hh))
        pygame.draw.line(self.win, (0, 255, 0), (xx, yy + hh), (xx + ww, yy + hh))
