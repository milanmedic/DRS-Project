import pygame


def draw_on_screen(image: object, screen: object, position: object) -> object:
    """ get rectangle of image"""
    box = image.get_rect()
    """    position[0]-rect.width//2  -> take the X coordinates where we want to put image and subtract half of image 
    width
    position[1]-rect.height//2 -> take the Y coordinates where we want to put image and subtract half of image  
    height     """
    box = box.move(position[0] - box.width // 2, position[1] - box.height // 2)
    """draw image, on position of box on screen"""
    screen.blit(image, box)


def rotate_entity(image, angle):
    location = image.get_rect().center
    new_image = pygame.transform.rotate(image, angle)
    new_image.get_rect().center = location
    return new_image
