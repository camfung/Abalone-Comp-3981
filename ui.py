from abc import ABC, abstractmethod
import pygame
import numpy as np

from enums import Marble


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface, gamestate):
        pass


class HUD(Drawable):
    def draw(self, surface, gamestate):
        # Example for drawing to the screen
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(10, 10, 150, 100))


class Board(Drawable):
    CELL_SIZE = 70
    MARGIN = 2
    OFFSET = CELL_SIZE / 2
    def draw(self, surface, gamestate):
        gamestate = gamestate.get_board()
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)
        GRAY = (128, 128, 128)
        BLUE = (0, 0, 255)

        screen = surface
        pygame.display.set_caption("Abalone Board")

        screen.fill(BLACK)

        for row in range(len(gamestate)):
                for col in range(len(gamestate[row])):
                    if gamestate[row][col] == Marble.NONE:
                        color = GRAY
                    elif gamestate[row][col] == Marble.BLACK:
                        color = BLUE
                    elif gamestate[row][col] == Marble.WHITE:
                        color = WHITE
                    else:
                        color = BLACK

                    # Calculate the offset
                    offset = self.OFFSET if row % 2 != 0 else 0  # Apply offset to odd rows for Abalone layout

                    pygame.draw.rect(
                        screen,
                        color,
                        [
                            (self.MARGIN + self.CELL_SIZE) * col + self.MARGIN + offset,
                            (self.MARGIN + self.CELL_SIZE) * row + self.MARGIN,
                            self.CELL_SIZE,
                            self.CELL_SIZE,
                        ],
                    )
    @classmethod
    def get_cell(cls, pos, game):
        board = game.get_board()
        for row in range(len(board)):
            for col in range(len(board[row])):
                offset = cls.OFFSET if row % 2 != 0 else 0
                rect = pygame.Rect(
                    (cls.MARGIN + cls.CELL_SIZE) * col + cls.MARGIN + offset,
                    (cls.MARGIN + cls.CELL_SIZE) * row + cls.MARGIN,
                    cls.CELL_SIZE,
                    cls.CELL_SIZE
                )
                if rect.collidepoint(pos):
                    return row, col
        return None, None


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

    def run(self, gamestate):
        pygame.init()
        while True:
            self.update(gamestate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    pos = pygame.mouse.get_pos()
                    row, col = Board.get_cell(pos, gamestate)
                    if row != None:
                        gamestate.get_board()[row][col] = 1

                    # left click
                    if event.button == 1:
                        print(f'Left click at {row, col}')

                    # right click
                    elif event.button == 3:
                        print(f'Right click at {row, col}')

    def update(self, gamestate):
        self.screen.fill((0, 0, 0))

        for element in self.elements:
            element.draw(self.screen, gamestate)

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
