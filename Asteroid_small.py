import pygame
import Loader
from Asteroid import Asteroid


class Asteroid_small(Asteroid):

    def __init__(self, position, screen_bounds, speed, direction):
        self.sizeofHitBox = 25
        self.resized_image = pygame.transform.scale(Loader.load_image("Asteroid_big.png"), (32, 32))
        super(Asteroid_small, self).__init__(self.resized_image, position, screen_bounds, speed,
                                             self.sizeofHitBox, direction, 200, "small", [10, 15])
