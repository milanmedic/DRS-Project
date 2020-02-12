import pygame
import os


def load_image(file_name):
    url = os.path.join('images', file_name)
    temp = pygame.image.load(url)
    retval = temp.convert_alpha()
    return retval


def load_sound(file_name):
    url = os.path.join('sounds', file_name)
    retval = pygame.mixer.Sound(url)
    return retval
