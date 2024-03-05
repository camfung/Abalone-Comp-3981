from abc import ABC, abstractmethod
import sys
import pygame
from enums import GameType, Marble
import pygame_menu
from enums import Formation, UIState
from ui_components import Button, Drawable, EventHandler


class HUD(Drawable, EventHandler):
    def __init__(self) -> None:
        super().__init__()

    def draw(self, surface, game_manager):
        # Example for drawing to the screen
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(10, 10, 150, 100))

    def handle_event(self, event):
        pass


class Board(Drawable, EventHandler):
    CELL_SIZE = 76
    SIDE_MARGIN = 13
    TOP_MARGIN = 2
    OFFSET = CELL_SIZE / 2 + SIDE_MARGIN - 5
    ALIGNMENT = [0, -2, -1, -1, 0, 0, 1, 1, 2, 2, 0]

    def __init__(self) -> None:
        super().__init__()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            row, col = Board.get_cell(pos)

            # left click
            if event.button == 1:
                print(f'Left click at {row, col}')
                print(pos)

            # right click
            elif event.button == 3:
                print(f'Right click at {row, col}')

    def draw(self, surface, game_manager):
        game_manager = game_manager.get_board()

        screen = surface
        pygame.display.set_caption("Abalone Board")

        background_image = pygame.image.load("images/final_board.png", "rb")
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        screen.blit(background_image, (0, 0))

        for row in range(len(game_manager)):
            for col in range(len(game_manager[row])):
                if game_manager[row][col] == Marble.BLACK:
                    ball_image = pygame.image.load("images/black_ball.png")
                elif game_manager[row][col] == Marble.WHITE:
                    ball_image = pygame.image.load("images/white_ball.png")
                else:
                    continue

                # Calculate the offset
                # Apply offset to odd rows for Abalone layout
                offset = self.OFFSET if row % 2 == 0 else 0
                total_grid_width = len(
                    game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.SIDE_MARGIN
                total_grid_height = len(
                    game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + \
                    (self.ALIGNMENT[row] + col) * \
                    (self.CELL_SIZE + self.SIDE_MARGIN) - offset
                cell_y = start_y + row * (self.CELL_SIZE + self.TOP_MARGIN)
                screen.blit(ball_image, (cell_x, cell_y))

    @classmethod
    def get_cell(cls, pos):
        board = cls.ALIGNMENT
        for row in range(len(board)):
            for col in range(len(board)):
                # Calculate the offset
                # Apply offset to odd rows for Abalone layout
                offset = cls.OFFSET if row % 2 == 0 else 0
                total_grid_width = len(
                    board) * cls.CELL_SIZE + (len(board) - 1) * cls.SIDE_MARGIN
                total_grid_height = len(
                    board) * cls.CELL_SIZE + (len(board) - 1) * cls.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + \
                    (cls.ALIGNMENT[row] + col) * \
                    (cls.CELL_SIZE + cls.SIDE_MARGIN) - offset
                cell_y = start_y + row * (cls.CELL_SIZE + cls.TOP_MARGIN)
                rect = pygame.Rect(
                    cell_x,
                    cell_y,
                    cls.CELL_SIZE,
                    cls.CELL_SIZE
                )
                if rect.collidepoint(pos):
                    return row, col
        return None, None


class UI(ABC):
    drawable_elements = []
    event_handlers = []

    # displays the board and the hud
    @abstractmethod
    def update(self, game_manager):
        pass


class PygameUI(UI):
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1300
    button_color = (0, 128, 255)
    button_highlight_color = (255, 255, 0)
    text_color = (255, 255, 255)

    def __init__(self, app) -> None:
        super().__init__()
        self.theme = pygame_menu.themes.THEME_DARK
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self._app = app

    def start_the_game(self, config):

        # Placeholder for starting the game with the selected configuration
        print(f"Starting game with config: {config}")

        def start_button_cb(): return self._app.notify(self, "MakeFirstMove")

        start_button = Button(1000, 100, 200, 50, PygameUI.button_color,
                              PygameUI.button_highlight_color, "Start", PygameUI.text_color, 32, start_button_cb)
        self.drawable_elements.append(start_button)
        self.event_handlers.append(start_button)
        self._app.notify(self, "StartGame", config=config)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self):
        pygame.init()
        self.main_menu()

    def update(self, game_manager):
        self.screen.fill((0, 0, 0))

        for element in self.drawable_elements:
            element.draw(self.screen, game_manager)

        pygame.display.flip()

    # In these methods we update the state in the board and the Hud and the changes are reflected by the update method
    def update_screen(self, game_manager):
        pass

    def display_score(self, record):
        pass

    def display_moves(self, record):
        pass

    def display_time_per_move(self, record):
        pass

    def display_board(self, game_manager):
        pass

    def main_menu(self):
        menu = pygame_menu.Menu('Welcome', PygameUI.SCREEN_WIDTH, PygameUI.SCREEN_HEIGHT,
                                theme=self.theme)

        menu.add.button('Play', self.play_menu)
        menu.add.button('Settings', self.settings_menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    def update_play_button(self, *args):
        print(args)
        # Logic to activate the play button based on selections
        pass

    def play_menu(self):
        menu = pygame_menu.Menu(
            'Play', PygameUI.SCREEN_WIDTH, PygameUI.SCREEN_HEIGHT, theme=self.theme)
        opponent_type = menu.add.selector(
            'Opponent: ', [('Human', GameType.PLAYER_VS_PLAYER), ('CPU', GameType.PLAYER_VS_CPU)])
        cpu_level = menu.add.dropselect('CPU Level: ', [(
            'Easy', 1), ('Medium', 2), ('Hard', 3)], default=1, onchange=self.update_play_button)
        formation = menu.add.dropselect('Formation: ', [(
            f.name, f) for f in Formation], default=0, onchange=self.update_play_button)

        menu.add.button('Play', lambda: self.start_the_game({'game_type': opponent_type.get_value(),
                                                             'cpu_level': cpu_level.get_value(),
                                                             'formation': formation.get_value()}))

        menu.add.button('Back', self.main_menu)
        menu.mainloop(self.screen)

    def settings_menu(self):
        menu = pygame_menu.Menu('Settings', self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
                                theme=self.theme)

        # Settings options will go here

        menu.add.button('Back', self.main_menu)
        menu.mainloop(self.screen)
