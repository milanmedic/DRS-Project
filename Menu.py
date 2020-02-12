import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
import Game
import Loader
import Howmany

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    START = 2
    ONEPL = 3
    TWOPL = 4
    THREEPL = 5
    FOURPL = 6


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """
    game_state = GameState.TITLE

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()
        self.action = action

    def update(self, mouse_pos, mouse_up):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]


def play_level(screen):
    return_btn = UIElement(
        center_position=(300, 600),
        font_size=20,
        bg_rgb=None,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    onepl = UIElement(
        center_position=(650, 300),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="1 player",
        action=GameState.ONEPL,
    )
    twopl = UIElement(
        center_position=(650, 350),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="2 players",
        action=GameState.TWOPL,
    )
    threepl = UIElement(
        center_position=(650, 400),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="3 players",
        action=GameState.THREEPL,
    )
    fourpl = UIElement(
        center_position=(650, 450),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="4 players",
        action=GameState.FOURPL,
    )

    buttons = [onepl, twopl, threepl, fourpl, return_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)
        image = Loader.load_image("Background.png")
        rect = image.get_rect()
        screen.blit(image, rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def title_screen(screen):
    game_title = UIElement(
        center_position=(650, 200),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="ASTEROIDS",
        action=GameState.TITLE,
    )
    start_btn = UIElement(
        center_position=(650, 400),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="Start",
        action=GameState.START,
    )
    quit_btn = UIElement(
        center_position=(650, 500),
        font_size=30,
        bg_rgb=None,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [game_title, start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)
        image = Loader.load_image("Background.png")
        rect = image.get_rect()
        screen.blit(image, rect)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    UIElement.game_state = GameState.TITLE

    while True:
        if UIElement.game_state == GameState.TITLE:
            UIElement.game_state = title_screen(screen)

        if UIElement.game_state == GameState.START:
            UIElement.game_state = play_level(screen)

        if UIElement.game_state == GameState.ONEPL:
            Howmany.igraci = 1
            Game.AsteroidsGame().run()

        if UIElement.game_state == GameState.TWOPL:
            Howmany.igraci = 2
            Game.AsteroidsGame().run()

        if UIElement.game_state == GameState.THREEPL:
            Howmany.igraci = 3
            Game.AsteroidsGame().run()

        if UIElement.game_state == GameState.FOURPL:
            Howmany.igraci = 4
            Game.AsteroidsGame().run()

        if UIElement.game_state == GameState.QUIT:
            pygame.quit()
            return


# call main when the script is run
if __name__ == "__main__":
    main()
