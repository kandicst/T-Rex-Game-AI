from src.Game import Game
import pygame
import neat, os


def run(config_path):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_path)
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #game = Game()
    winner = p.run(meth, 50)
    print('\nBest genome:\n{!s}'.format(winner))


def meth(genomes, config):
    game = Game()
    game.execute(genomes, config)

    pass

if __name__ == '__main__':

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
