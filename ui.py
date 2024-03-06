from abc import ABC, abstractmethod
import pygame
from enums import Marble
import pygame_menu
from enums import Formation, UIState

"""
Essentially what this interface is meant to do is replace the event handling in the pygameUI main game loop. 
The idea is that in the main game loop the handle event will be called on every event for all the ui components. 
The behavior for the events will be defined in the concrete class
"""


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface, game_manager):
        pass


class HUD(Drawable, EventHandler):
    HUD_WIDTH = 1000
    HUD_HEIGHT = 150
    menu = None

    def __init__(self):
        self.theme = pygame_menu.themes.THEME_DARK
        self.theme.widget_width = 100
        self.ui_instance = PygameUI()

    def create_hud(self):
        menu = pygame_menu.Menu("Abalone", self.HUD_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        # menu.add.button("Start Game", align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Stop Game", pygame_menu.events.EXIT, align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Pause", align=pygame_menu.locals.ALIGN_CENTER)  # TODO implementation
        menu.add.button("Reset", self.ui_instance.play_menu, align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Undo Last Move", align=pygame_menu.locals.ALIGN_CENTER)  # TODO implementation
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.label(f"White Score:    Black Score:    ") #TODO use Player.get_balls_remaining method

        return menu

    def get_menu(self):
        if self.menu is None:
            self.menu = self.create_hud()
        return self.menu

    def handle_event(self, event):
        pass

    def draw(self, surface, game_manager):
        menu = self.get_menu()
        menu.draw(surface)
        menu.update(pygame.event.get())


class Board(Drawable, EventHandler):
    CELL_SIZE = 76
    SIDE_MARGIN = 13
    TOP_MARGIN = 2
    OFFSET = CELL_SIZE / 2 + SIDE_MARGIN - 5
    ALIGNMENT = [0, -2, -1, -1, 0, 0, 1, 1, 2, 2, 0]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            row, col = Board.get_cell(pos)

            # left click
            if event.button == 1:
                print(f'Left click at {row, col}')

            # right click
            elif event.button == 3:
                print(f'Right click at {row, col}')

    def draw(self, surface, game_manager):
        game_manager = game_manager.get_board()

        screen = surface
        pygame.display.set_caption("Abalone Board")

        background_image = pygame.image.load("images/final_board.png", "rb")
        background_image = pygame.transform.scale(background_image, (1000, 1000))
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
                offset = self.OFFSET if row % 2 == 0 else 0  # Apply offset to odd rows for Abalone layout
                total_grid_width = len(game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.SIDE_MARGIN
                total_grid_height = len(game_manager) * self.CELL_SIZE + (len(game_manager) - 1) * self.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + (self.ALIGNMENT[row] + col) * (self.CELL_SIZE + self.SIDE_MARGIN) - offset
                cell_y = start_y + row * (self.CELL_SIZE + self.TOP_MARGIN)
                screen.blit(ball_image, (cell_x, cell_y))

    @classmethod
    def get_cell(cls, pos):
        board = cls.ALIGNMENT
        for row in range(len(board)):
            for col in range(len(board)):
                # Calculate the offset
                offset = cls.OFFSET if row % 2 == 0 else 0  # Apply offset to odd rows for Abalone layout
                total_grid_width = len(board) * cls.CELL_SIZE + (len(board) - 1) * cls.SIDE_MARGIN
                total_grid_height = len(board) * cls.CELL_SIZE + (len(board) - 1) * cls.TOP_MARGIN
                start_x = (1000 - total_grid_width) // 2
                start_y = (1000 - total_grid_height) // 2

                cell_x = start_x + (cls.ALIGNMENT[row] + col) * (cls.CELL_SIZE + cls.SIDE_MARGIN) - offset
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
    _instance = None
    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1000

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.theme = pygame_menu.themes.THEME_DARK
        self.screen = pygame.display.set_mode((1000, 1000))
        self.state = UIState.MAIN_MENU
        self.state_actions = {
            UIState.GAME_PLAY: self.run_game,
            UIState.MAIN_MENU: self.main_menu,
            UIState.SETTINGS_MENU: self.settings_menu,
            UIState.PLAY_MENU: self.play_menu,
        }

    def start_the_game(self, config):
        # Placeholder for starting the game with the selected configuration
        print(f"Starting game with config: {config}")
        self.run_game()

    def run_game(self):
        while True:
            self.update(self._game_manager)
            for event in pygame.event.get():
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def run(self, game_manager):
        self._game_manager = game_manager
        pygame.init()
        action = self.state_actions.get(self.state)
        if action:
            action()
        else:
            # Handle unknown state or default action
            print("Unknown state or default action")

    def update(self, game_manager):
        self.screen.fill((0, 0, 0))

        for element in self.drawable_elements:
            element.draw(self.screen, game_manager)

        pygame.display.flip()

    # In these methods we update the state in the board and the Hud and the changes are reflected by the update method
    def update_screen(self, game_manager):
        pass

    def display_score(self, game_manager):
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
            'Opponent: ', [('Human', 1), ('CPU', 2), ('CPU vs CPU', 3)])
        cpu_level = menu.add.dropselect('CPU Level: ', [(
            'Easy', 1), ('Medium', 2), ('Hard', 3)], default=1, onchange=self.update_play_button)
        formation = menu.add.dropselect('Formation: ', [(
            f.name, f) for f in Formation], default=0, onchange=self.update_play_button)

        menu.add.button('Play', lambda: self.start_the_game({'opponent_type': opponent_type.get_value(),
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

    def display_move_history(self):
        menu = pygame_menu.Menu("Move History", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, theme=self.theme)
        table = menu.add.table(table_id='records_table', font_size=20, font_color="Black")
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Turn #', 'White Moves', 'Black Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        # Hardcoded for now
        records = ["Example move"]

        # Modify this to match formatting of record history
        for index, record in enumerate(records, start=1):
            table.add_row([index - 1, record, record])

        menu.add.button('Back', self.run_game)
        menu.mainloop(self.screen)
