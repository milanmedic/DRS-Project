import pygame

import Loader
from Asteroid import Asteroid


class Asteroid_big(Asteroid):

    def __init__(self, position, screen_bounds, speed, direction):
        self.sizeofHitBox = 65
        self.resized_image = pygame.transform.scale(Loader.load_image("Asteroid_big.png"), (80, 80))
        super(Asteroid_big, self).__init__(self.resized_image, position, screen_bounds, speed,
                                           self.sizeofHitBox, direction, 100, "big", [30, 30])
