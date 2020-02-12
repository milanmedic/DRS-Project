import random
import BasicFunctions
import Loader
from GameEntity import GameEntity


class Asteroid(GameEntity):

    def __init__(self, image, position, screen_bounds, speed, size_of_hitbox, direction, score_value, asteroid_type, position_of_hitbox):
        super(Asteroid, self).__init__(position, image)
        self.asteroid_type = asteroid_type
        self.hitbox_pos = position_of_hitbox
        self.position = position
        self.sizeofHitBox = size_of_hitbox
        self.direction_xy = direction
        self.screen_bounds = screen_bounds
        self.speed = speed
        self.score_value = score_value
        self.hitbox = (self.position[0] - self.hitbox_pos[0], self.position[1]- self.hitbox_pos[1], size_of_hitbox, size_of_hitbox)

    def draw_on_screen(self, screen):
        BasicFunctions.draw_on_screen(self.image, screen, self.position)

    def move(self):
        move_x = self.direction_xy[0] * self.speed
        move_y = self.direction_xy[1] * self.speed

        self.position[0] += move_x
        self.position[1] += move_y

        if self.position[0] >= self.screen_bounds[0]:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = self.screen_bounds[0] - 1
        if self.position[1] >= self.screen_bounds[1]:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = self.screen_bounds[1] - 1

        self.hitbox = (self.position[0] - self.hitbox_pos[0], self.position[1]- self.hitbox_pos[1], self.sizeofHitBox, self.sizeofHitBox)
