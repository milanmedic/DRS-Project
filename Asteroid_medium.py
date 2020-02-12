import pygame
import Loader
from Asteroid import Asteroid


class Asteroid_medium(Asteroid):

    def __init__(self, position, screen_bounds, speed, direction):
        self.sizeofHitBox = 45
        self.resized_image = pygame.transform.scale(Loader.load_image("Asteroid_big.png"), (52, 52))
        super(Asteroid_medium, self).__init__(self.resized_image, position, screen_bounds, speed,
                                              self.sizeofHitBox, direction, 150, "medium", [20, 25])
