"""Trainer for NEAT-AI to play Flappy Bird."""
import os
import pygame
from typing import List
import neat
from app.game_objects import Bird, Pipe
from app import game_logic


def init_population(genomes, config):
    """Create birds, genomes, networks for NEAT training."""
    for _, g in genomes:
        g.fitness = 0
    nets = [neat.nn.FeedForwardNetwork.create(g, config) for _, g in genomes]
    birds = [Bird(230, 350) for _, _ in genomes]
    ge = [g for _, g in genomes]
    return birds, ge, nets


def change_fitness(ge: List, change_amount, indices=None):
    if indices is None:
        indices = range(len(ge))
    for i in indices:
        ge[i].fitness += change_amount


def eval_fitness(genomes, config):
    birds, ge, nets = init_population(genomes, config)
    window, ground, pipes = game_logic.create_window()

    score = 0
    while True:
        game_logic.handle_event()
        for i, bird in enumerate(birds):
            bird.move()
            change_fitness(ge, 0.1)
        game_logic.calc_birds_jump(birds, pipes, nets)
        ground.move()

        remove_list = game_logic.check_pipe_collision(birds, pipes)
        change_fitness(ge, -1, indices=remove_list)
        game_logic.drop_from_list(remove_list, birds, nets, ge)
        if game_logic.check_end_game(birds, score):
            break
        if game_logic.check_passed_pipe(pipes, birds[0]):
            score += 1
            change_fitness(ge, 5)
            game_logic.create_new_pipe(pipes)

        for pipe in pipes:
            pipe.move()

        game_logic.remove_old_pipe(pipes)
        birds_to_remove = game_logic.check_ground_collision(birds)
        game_logic.drop_from_list(birds_to_remove, birds, ge, nets)

        if game_logic.check_end_game(birds, score):
            break
        game_logic.draw_window(window, birds, pipes, ground, score)


def train(config_path: str):
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

    winner = population.run(eval_fitness, 50)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    train(config_path)


if __name__ == '__main__':
    main()
