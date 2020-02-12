import pygame
from GameEntity import GameEntity
import Loader
import BasicFunctions
import math
from Bullet import Bullet
import time


class Player(GameEntity):
    def __init__(self, position, screen_bounds, name, id):
        self.id = id
        if id == 1:
            super(Player, self).__init__(position, Loader.load_image('Spaceship_blue_0.png'))
            self.color = (0, 153, 255)
            self.image_1 = Loader.load_image('Spaceship_blue_1.png')
            self.image_2 = Loader.load_image('Spaceship_blue_2.png')
            self.image_3 = Loader.load_image('Spaceship_blue_3.png')
        if id == 2:
            super(Player, self).__init__(position, Loader.load_image('Spaceship_red_0.png'))
            self.color = (242, 32, 17)
            self.image_1 = Loader.load_image('Spaceship_red_1.png')
            self.image_2 = Loader.load_image('Spaceship_red_2.png')
            self.image_3 = Loader.load_image('Spaceship_red_3.png')
        if id == 3:
            super(Player, self).__init__(position, Loader.load_image('Spaceship_green_0.png'))
            self.color = (17, 242, 51)
            self.image_1 = Loader.load_image('Spaceship_green_1.png')
            self.image_2 = Loader.load_image('Spaceship_green_2.png')
            self.image_3 = Loader.load_image('Spaceship_green_3.png')
        if id == 4:
            super(Player, self).__init__(position, Loader.load_image('Spaceship_magenta_0.png'))
            self.color = (252, 30, 227)
            self.image_1 = Loader.load_image('Spaceship_magenta_1.png')
            self.image_2 = Loader.load_image('Spaceship_magenta_2.png')
            self.image_3 = Loader.load_image('Spaceship_magenta_3.png')
        self.name = name
        self.direction_xy = [0, 0]
        self.isMoving = False
        self.angle = 0
        self.max_speed = 3
        self.screen_bounds = screen_bounds
        self.bullets = []
        self.lives = 3
        self.score = 0
        self.godmode = 0
        self.now = time.time()
        self.future = self.now + 2
        self.hitbox = (self.direction_xy[0], self.direction_xy[1], 15, 22)

    def draw_on_screen(self, screen):
        if self.speed == 0:
            rotated_image = BasicFunctions.rotate_entity(self.image, self.angle)
            BasicFunctions.draw_on_screen(rotated_image, screen, self.position)
        elif 0 < self.speed <= self.max_speed * 0.5:
            rotated_image = BasicFunctions.rotate_entity(self.image_1, self.angle)
            BasicFunctions.draw_on_screen(rotated_image, screen, self.position)
        elif self.max_speed * 0.5 < self.speed < self.max_speed:
            rotated_image = BasicFunctions.rotate_entity(self.image_2, self.angle)
            BasicFunctions.draw_on_screen(rotated_image, screen, self.position)
        elif self.speed == self.max_speed:
            rotated_image = BasicFunctions.rotate_entity(self.image_3, self.angle)
            BasicFunctions.draw_on_screen(rotated_image, screen, self.position)

    def move(self):
        """x is moved by speed*cos(angle+90)      +90 because player starts at 90 (facing up)
           y is moved by speed*sin(angle+90)
           so new x coords are equal to old x plus xMoved
           new y coords are equal to old y plus yMoved
        """

        """x direction"""
        self.direction_xy[0] = math.cos(-math.radians(self.angle + 90))
        """y direction"""
        self.direction_xy[1] = -math.sin(math.radians(self.angle + 90))

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

        self.hitbox = (self.position[0] - 30, self.position[1] - 35, 60, 60)

    def turn(self, direction):
        if direction == "left":
            self.angle += 7
            self.angle %= 360
        elif direction == "right":
            self.angle -= 7
            self.angle %= 360

    def shoot(self):
        if self.id == 1:
            print('pew1')
        if self.id == 2:
            print('pew2')
        if self.id == 3:
            print('pew3')
        if self.id == 4:
            print('pew4')

        adjust = [0, 0]
        adjust[0] = math.sin(-math.radians(self.angle)) * self.image.get_width()
        adjust[1] = -math.cos(math.radians(self.angle)) * self.image.get_height()

        # create a new missile using the calculated adjusted position
        new_bullet = Bullet((self.position[0] + adjust[0], self.position[1] + adjust[1] / 2), self.angle)
        self.bullets.append(new_bullet)
