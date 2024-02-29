from abc import ABC, abstractmethod
import pygame


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass


class HUD(Drawable):
    def draw(self, surface):
        # Example for drawing to the screen
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(10, 10, 150, 100))


class Board(Drawable):
    def draw(self, surface):
        # Example for drawing to the screen
        pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(170, 10, 150, 100))


class UI(ABC):
    elements = []

    # displays the board and the hud
    @abstractmethod
    def update(self):
        pass


class PygameUI(UI):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.screen = pygame.display.set_mode((1000, 1000))

    def run(self):
        pygame.init()
        while True:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    pos = pygame.mouse.get_pos()

                    # left click
                    if event.button == 1:
                        print(f'Left click at {pos}')

                    # right click
                    elif event.button == 3:
                        print(f'Right click at {pos}')

    def update(self):
        self.screen.fill((0, 0, 0))

        for element in self.elements:
            element.draw(self.screen)

        pygame.display.flip()

    # In these methods we update the state in the board and the Hud and the changes are reflected by the update method
    def update_screen(self, game_state):
        pass

    def display_score(self, record):
        pass

    def display_moves(self, record):
        pass

    def display_time_per_move(self, record):
        pass

    def display_board(self, gameManager):
        pass
