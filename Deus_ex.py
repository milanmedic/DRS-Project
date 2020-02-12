from GameEntity import GameEntity
import pygame
import Loader
import time


class Deus_ex(GameEntity):

    def __init__(self, position):
        self.position = position
        self.state = 0
        self.sizeofHitBox = 40
        self.position_of_hitbox = [20, 20]
        self.image = Loader.load_image("question_mark.png")
        self.now = time.time()
        self.future = self.now + 2
        self.hitbox = (
        self.position[0] - self.position_of_hitbox[0], self.position[1] - self.position_of_hitbox[1], self.sizeofHitBox,
        self.sizeofHitBox)

    def transform(self):
        self.image = Loader.load_image("deus_ex.png")
        self.state = 1
