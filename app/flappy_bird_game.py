import os
import time
import random
import pygame
import neat


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500


BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join('images', f'bird{i}.png'))) for i in range(1, 4)]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0  # keeping track of time since last jump
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]

    def jump(self):
        self.velocity = -10.5  # Negative because origin is top left of window so vertical is reversed
        self.tick_count = 0  # reset when last jumped
        self.height = self.y

    def move(self):
        self.tick_count += 1  # incrementing 'time'

        # displacement is relative to location of last jump
        # y is absolute y position
        displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2
        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2
        self.y += displacement

        if (displacement < 0) or (self.y < self.height - 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    GAP = 200
    VELOCITY = 5
    PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
    PIPE_BOTTOM = PIPE_IMAGE

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))  # round for float point errs
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)  # None if no collision
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True
        return False


def draw_window(window, bird):
    window.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(window)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        draw_window(window, bird)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
