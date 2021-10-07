import os
from typing import Iterable
import pygame
import neat
from app.game_objects import Bird, Pipe, Ground, BACKGROUND_IMAGE
pygame.font.init()

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500
STAT_FONT = pygame.font.SysFont('comicsans', 50)


def draw_window(window: pygame.display, birds: Iterable[Bird], pipes: Iterable[Pipe], ground: Ground, score: int, gen: int):
    window.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)
    ground.draw(window)
    for bird in birds:
        bird.draw(window)

    text = STAT_FONT.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render(f'Generation: {gen}', True, (255, 255, 255))
    window.blit(text, (10, 10))

    pygame.display.update()


def run(config_path: str):
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


def eval_fitness(genomes, config, gen=0):
    for _, g in genomes:
        g.fitness = 0
    nets = [neat.nn.FeedForwardNetwork.create(g, config) for _, g in genomes]
    birds = [Bird(230, 350) for _, _ in genomes]
    ge = [g for _, g in genomes]

    ground = Ground(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    score = 0
    while running:
        # clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Get index of pipe in front of bird
        pipe_index = 0
        if len(birds) > 0:
            if (len(pipes) > 1) and (birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width())):
                pipe_index = 1  # second pipe if more than 1 pipe and past first pipe
        else:
            running = False
            break

        # Increase fitness based on time survived
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            output = nets[i].activate((
                bird.y,  # height of bird
                abs(bird.y - pipes[pipe_index].height),  # clearance with top pipe
                abs(bird.y - pipes[pipe_index].bottom),  # clearance with bottom pipe
            ))
            if output[0] > 0.5:
                bird.jump()

        ground.move()
        pipes_to_remove = []
        add_pipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                # Check collision
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                # Check if ready for new pipe
                if (not pipe.passed) and (pipe.x < bird.x):
                    pipe.passed = True
                    add_pipe = True
            # Check if pipe should be removed
            if (pipe.x + pipe.PIPE_TOP.get_width()) < 0:
                pipes_to_remove.append(pipe)
            pipe.move()

        # Add new pipe
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        # Remove old pipes
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # Check if bird hits ground
        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > 730 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        if score > 50:
            break
        draw_window(window, birds, pipes, ground, score, gen)


if __name__ == '__main__':
    LOCAL_DIR = os.path.dirname(__file__)
    CONFIG_PATH = os.path.join(LOCAL_DIR, "config-feedforward.txt")
    run(CONFIG_PATH)
