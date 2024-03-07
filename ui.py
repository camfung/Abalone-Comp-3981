from abc import ABC, abstractmethod
import sys
import pygame
from enums import Direction, GameType, Marble, PlayerInputEvents
import pygame_menu
from enums import Formation, UIState
from ui_components import Button, Drawable, EventHandler


class PlayerGameInputHandler:
    def __init__(self, callbacks):
        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None
        self.execute_move, self.is_marble_player_to_move = callbacks

    def set_is_marble_player_to_move_cb(self, cb):
        self.is_marble_player_to_move = cb

    def set_execute_move_cb(self, cb):
        self.execute_move = cb

    def on_marble_click(self, marble_position):

        # print("initial state: ", str(self))

        # first marble click
        if self.state == PlayerInputEvents.AWAITING_FIRST_MARBLE:
            self.__on_awaiting_first_marble(marble_position)

        # second marble click
        elif self.state == PlayerInputEvents.AWAITING_SECOND_MARBLE:
            self.__on_awaiting_second_marble(marble_position)

        # direction clicked for more than 1 marble move
        elif self.state == PlayerInputEvents.AWAITING_DIRECTION:
            self.__on_awaiting_direction(marble_position)
        # print("final state: ", str(self))

    def __on_awaiting_first_marble(self, marble_position):
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
        else:
            # do nothing
            pass

    def __on_awaiting_second_marble(self, marble_position):
        # print("second marble clicked")
        # clicked first_marble
        # so deselected it go back to awaiting first marble
        if self.first_marble == marble_position:
            self.first_marble = None
            self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE

        elif self.is_adjacent(self.first_marble, marble_position):

            # Here we handle a single marble move
            if self.is_valid_direction(self.first_marble, marble_position):
                self.second_marble = self.first_marble
                direction = self.calculate_direction(
                    self.first_marble, marble_position)
                self.execute_move(self.first_marble,
                                  self.second_marble, direction)
                self.reset_state()

            # handle second marble selected
            self.second_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_DIRECTION

    def __on_awaiting_direction(self, marble_position):
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
        else:
            direction = self.calculate_direction(
                self.second_marble, marble_position)
            if self.is_valid_direction(self.second_marble, marble_position):
                self.execute_move(self.first_marble,
                                  self.second_marble, direction)
                self.reset_state()
            else:
                # not a valid direction
                return

    def __str__(
        self): return f'{self.state}, First: {self.first_marble}, Second: {self.second_marble}'

    # checks if second positoin is within dist of first position
    def is_adjacent(self, first_position, second_position, dist=2):
        # Calculate row and column differences
        row_diff = abs(first_position[0] - second_position[0])
        col_diff = abs(first_position[1] - second_position[1])

        # Adjacency logic for a hexagonal grid
        if row_diff > dist or col_diff > dist:
            return False
        return True

    # checks if the to position is adjacent and not occupied
    def is_valid_direction(self, from_position, to_position):

        # check if occupied by your own
        if self.is_marble_player_to_move(to_position):
            return

        # Reuse is_adjacent logic for direction validity
        return self.is_adjacent(from_position, to_position, 1)

    def calculate_direction(self, from_position, to_position):
        # Direction is calculated based on row and column differences
        row_diff = to_position[0] - from_position[0]
        col_diff = to_position[1] - from_position[1]

        # Mapping differences to directions based on the Direction enum
        if row_diff == -1 and col_diff == 0:
            return Direction.UP_LEFT
        elif row_diff == -1 and col_diff == 1:
            return Direction.UP_RIGHT
        elif row_diff == 0 and col_diff == 1:
            return Direction.RIGHT
        elif row_diff == 1 and col_diff == 0:
            return Direction.DOWN_RIGHT
        elif row_diff == 1 and col_diff == -1:
            return Direction.DOWN_LEFT
        elif row_diff == 0 and col_diff == -1:
            return Direction.LEFT
        else:
            return None  # Invalid direction or positions are not adjacent

    def reset_state(self):
        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None


class HUD(Drawable, EventHandler):
    HUD_HEIGHT = 150
    menu = None

    def __init__(self, gui, callbacks):
        self.ui_instance = gui
        self.theme = self.ui_instance.theme
        self.theme.widget_width = 100

        start_game_cb, undo_move_cb, pause_game_cb = callbacks

    def create_hud(self):
        menu = pygame_menu.Menu("Abalone", self.ui_instance.SCREEN_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        # menu.add.button("Start Game", align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Stop Game", pygame_menu.events.EXIT,
                        align=pygame_menu.locals.ALIGN_CENTER)
        # TODO implementation
        menu.add.button("Pause", align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Reset", self.ui_instance.play_menu,
                        align=pygame_menu.locals.ALIGN_CENTER)
        # TODO implementation
        menu.add.button("Undo Last Move",
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)
        # TODO use Player.get_balls_remaining method
        menu.add.label(f"White Score:    Black Score:    ")

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
    TOP_OFFSET = 100
    TOP_MARGIN = 2
    OFFSET = CELL_SIZE / 2 + SIDE_MARGIN - 5
    ALIGNMENT = [0, -2, -1, -1, 0, 0, 1, 1, 2, 2, 0]

    def __init__(self, callbacks) -> None:
        super().__init__()
        self.waiting_for_player_input = False
        self.input_handler = PlayerGameInputHandler(callbacks)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            # handle input for players turn
            if self.waiting_for_player_input:
                row, col = Board.get_cell(pos)
                # print(f"({row}, {col})")
                # center_y, center_x = Board.get_circle_center(row, col)
                # print(center_x, center_y)
                # left click
                if event.button == 1:
                    if row is not None and col is not None:
                        self.input_handler.on_marble_click((row, col))
                # right click
                elif event.button == 3:
                    self.input_handler.reset_state()

    def draw(self, surface, game_manager):
        game_manager = game_manager.get_board()

        screen = surface
        pygame.display.set_caption("Abalone Board")

        background_image = pygame.image.load("images/final_board.png", "rb")
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        screen.blit(background_image, (0, self.TOP_OFFSET))

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
                cell_y = start_y + row * \
                    (self.CELL_SIZE + self.TOP_MARGIN) + self.TOP_OFFSET
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
                cell_y = start_y + row * \
                    (cls.CELL_SIZE + cls.TOP_MARGIN) + cls.TOP_OFFSET
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
        self.start_button_clicked = False
        def start_game_cb(): return self._app.notify(self, "AiMakeMove")
        def undo_move_cb(): return self._app.notify(self, "UndoLastMove")
        def pause_game_cb(): return self._app.notfy(self, "PauseGame")
        callbacks = (
            start_game_cb,
            undo_move_cb,
            pause_game_cb,
        )
        hud = HUD(self, callbacks)

        def execute_move_cb(first_marble, second_marble, direction):
            return self._app.notify(self, "PlayerMakeMove", first_marble=first_marble,
                                    second_marble=second_marble, direction=direction)

        def marble_player_to_move_cb(marble_pos):
            return self._app.notify(self, "IsMarblePlayerToMove", marble_pos=marble_pos)
        callbacks = (
            execute_move_cb,
            marble_player_to_move_cb
        )
        board = Board(callbacks)
        self.board = board

        # add the drawables
        self.drawable_elements.append(hud)
        self.drawable_elements.append(board)

        # add the event handlers
        self.event_handlers.append(hud)
        self.event_handlers.append(board)

    def start_the_game(self, config):

        # Placeholder for starting the game with the selected configuration
        # print(f"Starting game with config: {config}")

        def start_button_cb(): return self._app.notify(self, "AiMakeMove")

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

    @property
    def waiting_for_player_input(self):
        return self.board.waiting_for_player_input

    @waiting_for_player_input.setter
    def waiting_for_player_input(self, value):
        self.board.waiting_for_player_input = value

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
        # print(args)
        # Logic to activate the play button based on selections
        pass

    def play_menu(self):
        menu = pygame_menu.Menu(
            'Play', PygameUI.SCREEN_WIDTH, PygameUI.SCREEN_HEIGHT, theme=self.theme)
        opponent_type = menu.add.selector(
            'Opponent: ', [('CPU', GameType.PLAYER_VS_CPU), ('Human', GameType.PLAYER_VS_PLAYER)])
        cpu_level = menu.add.dropselect('Agent:     ', [(
            'Random moves', 1), ('Cameron', 2), ('Joey', 3), ('Elsa', 4), ('Callum', 5)], default=0, onchange=self.update_play_button)
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

    def display_move_history(self):
        menu = pygame_menu.Menu(
            "Move History", self.SCREEN_WIDTH, self.SCREEN_HEIGHT, theme=self.theme)
        table = menu.add.table(table_id='records_table',
                               font_size=20, font_color="Black")
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
