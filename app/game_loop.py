import os
import pygame
from typing import List
import neat
from game_logic import Game
from game_objects import Bird
import trainer


class GameLoop:
    game: Game
    ge: neat.genome
    nets: neat.nn.FeedForwardNetwork
    CLOCK = pygame.time.Clock()

    def __init__(self, trained_bird: Bird = None, train_model: bool = False):
        self.train_model = train_model
        if trained_bird is None:
            if not self.train_model:
                birds = [Bird(230, 350)]
                self.game = Game(birds)

    def game_loop(self):
        while True:
            self.CLOCK.tick(30)
            self.game.handle_event()
            for i, bird in enumerate(self.game.birds):
                bird.move()
                if self.train_model:
                    trainer.change_fitness(self.ge, 0.1)
            if self.train_model:
                trainer.calc_birds_jump(self.game.birds, self.game.pipes, self.nets)
            self.game.ground.move()
            remove_list = self.game.check_pipe_collision()
            self.game.drop_from_list(remove_list, self.game.birds)
            if self.train_model:
                trainer.change_fitness(self.ge, -1, indices=remove_list)
                self.game.drop_from_list(remove_list, self.nets, self.ge)

            if self.game.check_end_game():
                break
            if self.game.check_passed_pipe():
                self.game.score += 1
                if self.train_model:
                    trainer.change_fitness(self.ge, 5)
                self.game.create_new_pipe()
            for pipe in self.game.pipes:
                pipe.move()
            self.game.remove_old_pipe()
            birds_to_remove = self.game.check_ground_collision()
            self.game.drop_from_list(
                birds_to_remove,
                self.game.birds,
                self.game.pipes,
            )
            if self.game.check_end_game():
                break
            self.game.draw_window()

    def play(self):
        self.game_loop()

    def train(self, genomes, config):
        birds, self.ge, self.nets = trainer.init_population(genomes, config)
        self.game = Game(birds)


def main():
    game = GameLoop()
    game.play()


if __name__ == '__main__':
    main()