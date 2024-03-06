from abc import ABC, abstractmethod
import sys
import pygame
from enums import Direction, GameType, Marble, PlayerInputEvents
import pygame_menu
from enums import Formation, UIState
from ui_components import Button, Drawable, EventHandler


class PlayerGameInputHandler:
    def __init__(self):
        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None
        self.execute_move = None
        self.is_marble_player_to_move = None

    def set_is_marble_player_to_move_cb(self, cb):
        self.is_marble_player_to_move = cb

    def set_execute_move_cb(self, cb):
        self.execute_move = cb

    def on_marble_click(self, marble_position):

        # clicking on a non marble
        print("marbleClicked is player to move: ",
              self.is_marble_player_to_move(marble_position))
        # first marble click
        if self.state == PlayerInputEvents.AWAITING_FIRST_MARBLE:
            print("first marble clicked ")
            self.first_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE

        # second marble click
        elif self.state == PlayerInputEvents.AWAITING_SECOND_MARBLE:
            print("second marble clicked")
            if self.is_adjacent(self.first_marble, marble_position):
                # Here we handle a single marble move
                self.second_marble = self.first_marble
                direction = self.calculate_direction(
                    self.first_marble, marble_position)
                if direction is not None:
                    self.execute_move(self, "PlayerMakeMove", first_marble=self.first_marble,
                                      second_marble=self.second_marble, direction=direction)
                    self.reset_state()
                else:
                    # Handle invalid direction (optional)
                    pass

            # clicked the first one clicked
            # so deslected it
            elif self.first_marble == marble_position:
                self.first_marble = None
                self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
            else:
                self.first_marble = marble_position
                # Remain in AWAITING_SECOND_MARBLE state for a new second selection

        # direction clicked for more than 1 marble move
        elif self.state == PlayerInputEvents.AWAITING_DIRECTION:
            # This block may no longer be necessary for single marble moves
            # but kept for handling moves involving more than one marble.
            print("direction clicked")
            if self.is_valid_direction(self.second_marble, marble_position):
                direction = self.calculate_direction(
                    self.second_marble, marble_position)
                self.execute_move(self, "PlayerMakeMove", first_marble=self.first_marble,
                                  second_marble=self.second_marble, direction=direction)
                self.reset_state()

            # if first or second marble are selected then we set the first marble to be the user selected marble
            elif self.second_marble == marble_position or self.first_marble == marble_position:
                self.first_marble = marble_position
                self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
            else:
                # Invalid direction selection; maybe handle error or prompt user
                pass

    def is_adjacent(self, first_position, second_position):
        # Calculate row and column differences
        row_diff = abs(first_position[0] - second_position[0])
        col_diff = abs(first_position[1] - second_position[1])

        # Adjacency logic for a hexagonal grid
        if row_diff > 1 or col_diff > 1:
            return False
        if row_diff == 1 and col_diff == 1:
            return False
        return True

    def is_valid_direction(self, from_position, to_position):
        # Reuse is_adjacent logic for direction validity
        return self.is_adjacent(from_position, to_position)

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
        self.waiting_for_player_input = False
        self.input_handler = PlayerGameInputHandler()

    def set_marble_player_to_move(self, cb):
        self.input_handler.set_is_marble_player_to_move_cb(cb)

    def set_execute_move_cb(self, cb):
        self.input_handler.set_execute_move_cb(cb)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()
            # handle input for players turn
            if self.waiting_for_player_input:
                row, col = Board.get_cell(pos)
                print(f"({row}, {col})")
                # left click
                if event.button == 1:
                    if row is not None and col is not None:
                        self.input_handler.on_marble_click(pos)
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
        self.start_button_clicked = False

        hud = HUD()
        board = Board()

        # add the drawables
        self.drawable_elements.append(hud)
        self.drawable_elements.append(board)

        # add the event handlers
        self.event_handlers.append(hud)
        self.event_handlers.append(board)

        self.board = board

        board.set_execute_move_cb(
            lambda move: self._app.notify(self, "PlayerMakeMove", move=move))
        board.set_marble_player_to_move(
            lambda marble_pos: self._app.notify(self, "IsMarblePlayerToMove", marble_pos=marble_pos))

    def start_the_game(self, config):

        # Placeholder for starting the game with the selected configuration
        print(f"Starting game with config: {config}")

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
            'Opponent: ', [('CPU', GameType.PLAYER_VS_CPU), ('Human', GameType.PLAYER_VS_PLAYER)])
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
