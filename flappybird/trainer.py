"""Trainer for NEAT-AI to play Flappy Bird."""
import os
import pygame
from typing import List, Callable, Any
import neat
from flappybird.game_objects import Bird, Pipe
from flappybird import game_logic
from flappybird import game_loop


def init_population(genomes, config) -> (List[Bird], neat.DefaultGenome, neat.nn.FeedForwardNetwork):
    """Create birds, genomes, networks for NEAT training."""
    for _, g in genomes:
        g.fitness = 0
    nets = [neat.nn.FeedForwardNetwork.create(g, config) for _, g in genomes]
    birds = [Bird(230, 350) for _, _ in genomes]
    ge = [g for _, g in genomes]
    return birds, ge, nets


def change_fitness(ge: List, change_amount: float, indices=None) -> None:
    if indices is None:
        indices = range(len(ge))
    for i in indices:
        ge[i].fitness += change_amount


def calc_birds_jump(birds: List[Bird], next_pipe: Pipe, nets: neat.nn.FeedForwardNetwork) -> None:
    for i, bird in enumerate(birds):
        output = nets[i].activate((
            bird.y,
            abs(bird.y - next_pipe.height),
            abs(bird.y - next_pipe.bottom),
        ))
        if output[0] > 0.5:  # output is a tuple, need first item
            bird.jump()


def train(config_path: str, training_func: Callable[[neat.genome, neat.nn.FeedForwardNetwork], Any]):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(training_func, 50)


def main():
    game_loop.train()


if __name__ == '__main__':
    main()
