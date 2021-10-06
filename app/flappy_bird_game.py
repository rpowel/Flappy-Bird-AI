import os
from typing import Iterable
import pygame
import neat
from app.game_objects import Bird, Pipe, Ground


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))


def draw_window(window: pygame.display, bird: Bird, pipes: Iterable[Pipe], ground: Ground):
    window.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    ground.draw(window)
    bird.draw(window)

    pygame.display.update()


def main():
    bird = Bird(230, 350)
    ground = Ground(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        ground.move()
        pipes_to_remove = []
        add_pipe = False
        for pipe in pipes:
            # Check collision
            if pipe.collide(bird):
                pass
            # Check if pipe should be removed
            if (pipe.x + pipe.PIPE_TOP.get_width()) < 0:
                pipes_to_remove.append(pipe)
            # Check if ready for new pipe
            if (not pipe.passed) and (pipe.x < bird.x):
                pipe.passed = True
                add_pipe = True

            pipe.move()

        # Add new pipe
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        # Remove old pipes
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # Check if bird hits ground
        if (bird.y + bird.image.get_height()) > 730:
            pass
        draw_window(window, bird, pipes, ground)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
