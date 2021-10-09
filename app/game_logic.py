"""Primary game logic for Flappy Bird game."""
import os
from typing import List
import pygame
import neat
from app.game_objects import Bird, Pipe, Ground, BACKGROUND_IMAGE
pygame.font.init()


class Game:
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 500
    STAT_FONT = pygame.font.SysFont('comicsans', 50)
    GENERATION = 1

    def __init__(self):
        self.window = None
        self.ground = None
        self.pipes = None
        self.birds = []
        self.score = 0
        self.clock = pygame.time.Clock()

    def game_loop(self):
        self.window, self.ground, self.pipes = self.create_window()
        self.birds = [Bird(230, 350)]
        self.score = 0
        while True:
            self.clock.tick(30)
            self.handle_event()
            # for bird in self.birds:
                # bird.move()
            self.ground.move()
            remove_list = self.check_pipe_collision()
            self.drop_from_list(remove_list, self.birds)
            if self.check_end_game():
                break
            if self.check_passed_pipe():
                self.score += 1
                self.create_new_pipe()
            for pipe in self.pipes:
                pipe.move()
            self.remove_old_pipe()
            remove_list = self.check_ground_collision()
            self.drop_from_list(remove_list, self.birds)
            if self.check_end_game():
                break
            self.draw_window()

    def check_end_game(self) -> bool:
        """Check if game should be ended."""
        if (self.score > 20) or (len(self.birds) == 0):
            return True
        return False

    def create_window(self):
        window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        ground = Ground(730)
        pipes = [Pipe(600)]
        return window, ground, pipes

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.K_SPACE:
                self.birds[0].jump()

    def get_next_pipe_index(self) -> int:
        pipe_index = 0
        if len(self.birds) > 0:
            if (len(self.pipes) > 1) and (self.birds[0].x > (self.pipes[0].x + pipes[0].PIPE_TOP.get_width())):
                pipe_index = 1  # second pipe if more than 1 pipe and past first pipe
        return pipe_index

    def check_ground_collision(self):
        i_list = []
        for i, bird in enumerate(self.birds):
            if (bird.y + bird.image.get_height()) > 730 or bird.y < 0:
                i_list.append(i)
        return i_list

    def check_pipe_collision(self):
        i_list = []
        for pipe in self.pipes:
            for i, bird in enumerate(self.birds):
                if pipe.collide(bird):
                    i_list.append(i)
        return i_list

    def check_passed_pipe(self):
        for pipe in self.pipes:
            if (not pipe.passed) and (pipe.x < self.birds[0].x):
                pipe.passed = True
                return True
        return False

    @staticmethod
    def drop_from_list(indices_to_drop: List[int], *args):
        for i in sorted(indices_to_drop, reverse=True):
            for lst in args:
                lst.pop(i)

    def remove_old_pipe(self) -> None:
        for pipe in self.pipes:
            if (pipe.x + pipe.PIPE_TOP.get_width()) < 0:
                self.pipes.pop(0)

    def create_new_pipe(self):
        self.pipes.append(Pipe(600))

    def draw_window(self):
        self.window.blit(BACKGROUND_IMAGE, (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.window)
        self.ground.draw(self.window)
        for bird in self.birds:
            bird.draw(self.window)

        text = self.STAT_FONT.render(f'Score: {self.score}', True, (255, 255, 255))
        self.window.blit(text, (self.WINDOW_WIDTH - 10 - text.get_width(), 10))

        pygame.display.update()


def main():
    game = Game()
    game.game_loop()


if __name__ == '__main__':
    main()
