import BasicFunctions
import Loader
from GameEntity import GameEntity
import math


class Bullet(GameEntity):
    def __init__(self, position, angle):
        super(Bullet, self).__init__(position, Loader.load_image('missile.png'))

        self.direction_xy = [position[0], position[1]]
        self.angle = angle
        self.max_speed = 3
        self.move_x = 0
        self.move_y = 0
        self.hitbox = (self.direction_xy[0], self.direction_xy[1], 15, 22)

    def draw_on_screen(self, screen):
        rotated_image = BasicFunctions.rotate_entity(self.image, self.angle)
        BasicFunctions.draw_on_screen(rotated_image, screen, self.direction_xy)

    def move(self):
        self.move_x = math.cos(-math.radians(self.angle + 90))
        self.move_y = -math.sin(math.radians(self.angle + 90))

        move_x = self.move_x * self.max_speed
        move_y = self.move_y * self.max_speed

        self.direction_xy[0] += move_x
        self.direction_xy[1] += move_y
        self.hitbox = (self.direction_xy[0]-5, self.direction_xy[1]-15, 10, 30)
