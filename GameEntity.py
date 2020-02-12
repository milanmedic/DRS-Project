import pygame
import BasicFunctions


class GameEntity(object):
    """All game entities ( player, asteroids, bullets)"""

    def __init__(self, position, image, speed=0):
        self.image = image
        self.position = list(position[:])
        self.speed = speed

    def size(self):
        return max(self.image.get_height(), self.image.get_width())

    def draw_on(self, screen):
        BasicFunctions.draw_on_screen(self.image, screen, self.position)
