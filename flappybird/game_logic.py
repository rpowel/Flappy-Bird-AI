"""Primary game logic for Flappy Bird game."""
import pygame

from typing import List

from flappybird.game_objects import Bird, Pipe, Ground, BACKGROUND_IMAGE

pygame.font.init()


class Game:
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 500
    STAT_FONT = pygame.font.SysFont('comicsans', 50)
    GENERATION = 1
    PIPES: Pipe

    def __init__(self, birds: List[Bird]):
        self.window, self.ground, self.pipes = self.create_window()
        self.birds = birds
        self.score = 0

    def check_end_game(self) -> bool:
        """Check if game should be ended."""
        if (self.score > 10) or (len(self.birds) == 0):
            return True
        return False

    def create_window(self) -> (pygame.Surface, Ground, Pipe):
        window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        ground = Ground(730)
        pipes = [Pipe(600)]
        return window, ground, pipes

    def handle_event(self, train_model: bool) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif (event.type == pygame.KEYDOWN) and (not train_model):
                if event.key == pygame.K_SPACE:
                    self.birds[0].jump()

    def get_next_pipe_index(self) -> int:
        pipe_index = 0
        if len(self.birds) > 0:
            if (len(self.pipes) > 1) and (self.birds[0].x > (self.pipes[0].x + self.pipes[0].PIPE_TOP.get_width())):
                pipe_index = 1  # second pipe if more than 1 pipe and past first pipe
        return pipe_index

    def check_ground_collision(self) -> List[int]:
        i_list = []
        for i, bird in enumerate(self.birds):
            if (bird.y + bird.image.get_height()) > 730 or bird.y < 0:
                i_list.append(i)
        return i_list

    def check_pipe_collision(self) -> List[int]:
        i_list = []
        for pipe in self.pipes:
            for i, bird in enumerate(self.birds):
                if pipe.collide(bird):
                    i_list.append(i)
        return i_list

    def check_passed_pipe(self) -> bool:
        for pipe in self.pipes:
            if (not pipe.passed) and (pipe.x < self.birds[0].x):
                pipe.passed = True
                return True
        return False

    @staticmethod
    def drop_from_list(indices_to_drop: List[int], *args) -> None:
        for i in sorted(indices_to_drop, reverse=True):
            for lst in args:
                lst.pop(i)

    def remove_old_pipe(self) -> None:
        for pipe in self.pipes:
            if (pipe.x + pipe.PIPE_TOP.get_width()) < 0:
                self.pipes.pop(0)

    def create_new_pipe(self) -> None:
        self.pipes.append(Pipe(600))

    def draw_window(self) -> None:
        self.window.blit(BACKGROUND_IMAGE, (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.window)
        self.ground.draw(self.window)
        for bird in self.birds:
            bird.draw(self.window)

        text = self.STAT_FONT.render(f'Score: {self.score}', True, (255, 255, 255))
        self.window.blit(text, (self.WINDOW_WIDTH - 10 - text.get_width(), 10))

        pygame.display.update()
