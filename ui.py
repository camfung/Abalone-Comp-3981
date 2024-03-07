from abc import ABC, abstractmethod
import sys
import pygame
from enums import Direction, GameType, Marble, PlayerInputEvents
import pygame_menu
from enums import Formation, UIState
from records import RecordHistory
from ui_components import Button, Drawable, EventHandler


class PlayerGameInputHandler:
    def __init__(self, callbacks):
        """
        Initialize the game input handler with specific callbacks.

        Parameters:
        - callbacks (tuple): A tuple containing two functions, execute_move and is_marble_player_to_move,
          used to handle game logic and check if a marble belongs to the player making the move.
        """

        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None
        self.execute_move, self.is_marble_player_to_move, self.update_board = callbacks

    def on_marble_click(self, marble_position):
        """
        Handle marble click events based on the current state of the game.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
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
        print("final state: ", str(self))

    def __on_awaiting_first_marble(self, marble_position):
        """
        Handle the event when awaiting the first marble selection.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.state = PlayerInputEvents.AWAITING_SECOND_MARBLE
        else:
            # do nothing
            pass

    def __on_awaiting_second_marble(self, marble_position):
        """
        Handle the event when awaiting the second marble selection.

        Parameters:
        - marble_position (tuple): The position of the marble that was clicked.
        """
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
        """
        Handle the event when awaiting the direction selection after selecting two marbles.

        Parameters:
        - marble_position (tuple): The position of the direction or third marble clicked.
        """
        if self.is_marble_player_to_move(marble_position):
            self.first_marble = marble_position
            self.second_marble = None
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

    def __str__(self):
        """
        Returns a string representation of the current game state.

        Returns:
        - str: A string representation of the current game state.
        """
        return f'{self.state}, First: {self.first_marble}, Second: {self.second_marble}'

    # checks if second positoin is within dist of first position
    def is_adjacent(self, first_position, second_position, dist=2):
        """
        Check if two positions are adjacent based on a specified distance.

        Parameters:
        - first_position (tuple): The first position.
        - second_position (tuple): The second position.
        - dist (int): The maximum distance for two positions to be considered adjacent.

        Returns:
        - bool: True if the positions are adjacent, False otherwise.
        """
        # Calculate row and column differences
        row_diff = abs(first_position[0] - second_position[0])
        col_diff = abs(first_position[1] - second_position[1])

        # Adjacency logic for a hexagonal grid
        if row_diff > dist or col_diff > dist:
            return False
        return True

    # checks if the to position is adjacent and not occupied
    def is_valid_direction(self, from_position, to_position):
        """
        Check if moving from one position to another is a valid direction and not occupied by the player's own marble.

        Parameters:
        - from_position (tuple): The starting position.
        - to_position (tuple): The target position.

        Returns:
        - bool/None: True if the direction is valid, False or None otherwise.
        """

        # check if occupied by your own
        if self.is_marble_player_to_move(to_position):
            return

        # Reuse is_adjacent logic for direction validity
        return self.is_adjacent(from_position, to_position, 1)

    def calculate_direction(self, from_position, to_position):
        """
        Calculate the direction of movement from one position to another.

        Parameters:
        - from_position (tuple): The starting position.
        - to_position (tuple): The target position.

        Returns:
        - Direction: The direction of movement.
        """
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
        """
        Reset the game state to its initial conditions, awaiting the first marble selection.
        """
        self.state = PlayerInputEvents.AWAITING_FIRST_MARBLE
        self.first_marble = None
        self.second_marble = None



class HUD(Drawable, EventHandler):
    """
    A Heads-Up Display (HUD) class that handles the creation and management of the game's interface elements.
    It extends both Drawable and EventHandler interfaces to allow for drawing the HUD and handling input events.
    """
    HUD_HEIGHT = 150
    menu = None

    def __init__(self, gui, callbacks):
        """
        Initializes the HUD with a reference to the GUI instance and a tuple of callback functions.

        Parameters:
        - gui: An instance of the GUI class, used to access GUI-related attributes and methods.
        - callbacks: A tuple containing references to callback functions for game actions like start, undo, and pause.
        """
        self.ui_instance = gui
        self.theme = self.ui_instance.theme
        self.theme.widget_width = 100
        self.score_label = None
        self._white_balls = 0
        self._black_balls = 0

        self.start_game_cb, self.undo_move_cb, self.pause_game_cb = callbacks

    def create_hud(self):
        """
        Creates the HUD menu with game control buttons like start, stop, pause, reset, undo last move, and show move history.

        Returns:
        - menu: A pygame_menu.Menu instance representing the HUD with all the control buttons.
        """
        menu = pygame_menu.Menu("Abalone", self.ui_instance.SCREEN_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        menu.add.button("Start Game", self.start_game_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Stop Game", pygame_menu.events.EXIT,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Pause", self.pause_game_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Reset", self.ui_instance.play_menu,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Undo Last Move", self.undo_move_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)
        self.score_label = menu.add.label(
            f"White Score: {self._white_balls}   Black Score:  {self._black_balls}  ")

        return menu

    @property
    def white_balls(self):
        """
        Property getter for the number of white balls.

        Returns:
        - _white_balls: The current number of white balls.
        """
        return self._white_balls

    @white_balls.setter
    def white_balls(self, value):
        """
        Property setter for the number of white balls. Updates the score label with the new value.

        Parameters:
        - value: The new number of white balls.
        """
        self._white_balls = value
        if self.score_label is not None:
            self.score_label.set_title(
                f"White Score: {self._white_balls}   Black Score:  {self._black_balls}  ")

    @property
    def black_balls(self):
        """
        Property getter for the number of black balls.

        Returns:
        - _black_balls: The current number of black balls.
        """
        return self._black_balls

    @black_balls.setter
    def black_balls(self, value):
        """
        Property setter for the number of black balls. Updates the score label with the new value.

        Parameters:
        - value: The new number of black balls.
        """
        self._black_balls = value
        if self.score_label is not None:
            self.score_label.set_title(
                f"White Score: {self._white_balls}   Black Score:  {self._black_balls}  ")

    def get_menu(self):
        """
        Retrieves the HUD menu, creating it if it does not already exist.

        Returns:
        - menu: The pygame_menu.Menu instance representing the HUD.
        """
        if self.menu is None:
            self.menu = self.create_hud()
        return self.menu

    def handle_event(self, event):
        """
        Handles an input event, passing it to the HUD menu for processing.

        Parameters:
        - event: The event to be handled, typically from the pygame event queue.
        """
        menu = self.get_menu()
        menu.update([event])

    def draw(self, surface, game_manager):
        """
        Draws the HUD menu onto the specified surface.

        Parameters:
        - surface: The pygame surface to draw the HUD on.
        - game_manager: The game manager instance, used to access game-related data and methods.
        """
        menu = self.get_menu()
        menu.draw(surface)


class Board(Drawable, EventHandler):
    """
    A class representing the game board, responsible for drawing the board and handling events related to it.
    It implements the Drawable and EventHandler interfaces for graphical display and event handling, respectively.
    """

    CELL_SIZE = 76
    SIDE_MARGIN = 13
    TOP_OFFSET = 100
    TOP_MARGIN = 2
    OFFSET = CELL_SIZE / 2 + SIDE_MARGIN - 5
    ALIGNMENT = [0, -2, -1, -1, 0, 0, 1, 1, 2, 2, 0]

    def __init__(self, callbacks) -> None:
        """
        Initializes the Board class with callback functions for handling game inputs.

        Parameters:
        - callbacks: A tuple or list containing callback functions to handle various player actions.
        """
        super().__init__()
        self.waiting_for_player_input = False
        self.input_handler = PlayerGameInputHandler(callbacks)

    def handle_event(self, event):
        """
        Handles user input events, specifically mouse button presses for selecting marbles or resetting the game state.

        Parameters:
        - event: The event to be handled, usually a mouse event from the pygame event queue.
        """
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
    def clicked_marbles(self, first_ball, second_ball):
        row1, col1 = first_ball
        row2, col2 = second_ball

        returned_array = []

        # Check if positions are in the same row
        if row1 == row2:
            new_ball = [(row1, col) for col in range(min(col1, col2) + 1, max(col1, col2))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # Check if positions are in the same column
        if col1 == col2:
            new_ball = [(row, col1) for row in range(min(row1, row2) + 1, max(row1, row2))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # Check if positions are in the same diagonal
        if abs(row1 - row2) == abs(col1 - col2):
            # Determine the direction of the diagonal
            row_step = 1 if row1 < row2 else -1
            col_step = 1 if col1 < col2 else -1

            # Collect locations in the diagonal
            new_ball = [(row, col) for row, col in zip(range(row1 + row_step, row2, row_step),
                                                   range(col1 + col_step, col2, col_step))]
            if len(new_ball) > 0:
                returned_array.append(new_ball[0])
            returned_array.append((row2, col2))
            returned_array.append((row1, col1))
            return returned_array

        # No straight line found
        return []


    def draw(self, surface, game_manager):
        """
        Draws the game board, including the background and marbles, onto the specified surface.

        Parameters:
        - surface: The pygame Surface object where the board should be drawn.
        - game_manager: An instance of the GameManager class, used to access the current state of the game board.
        """
        game_manager = game_manager.get_board()
        clicks = []

        screen = surface
        pygame.display.set_caption("Abalone Board")

        if self.input_handler.first_marble != None:
            if self.input_handler.second_marble != None:
                clicks = self.clicked_marbles(self.input_handler.first_marble, self.input_handler.second_marble)
            else:
                clicks.append(self.input_handler.first_marble)
        else:
            clicks = []

        background_image = pygame.image.load("images/final_board.png", "rb")
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        background_image = pygame.transform.scale(
            background_image, (1000, 1000))
        screen.blit(background_image, (0, self.TOP_OFFSET))

        for row in range(len(game_manager)):
            for col in range(len(game_manager[row])):
                if game_manager[row][col] == Marble.BLACK:
                    if (row, col) in clicks:
                        ball_image = pygame.image.load("images/dark_black_ball.png")
                    else:
                        ball_image = pygame.image.load("images/black_ball.png")
                elif game_manager[row][col] == Marble.WHITE:
                    if (row, col) in clicks:
                        ball_image = pygame.image.load("images/dark_white_ball.png")
                    else:
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
        """
        Calculates which cell of the board is at a given pixel position.

        Parameters:
        - pos: A tuple containing the (x, y) coordinates of the pixel position.

        Returns:
        - A tuple (row, col) indicating the cell's row and column. Returns (None, None) if the position is outside any cell.
        """
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
    """
    An abstract base class representing the user interface (UI) of the game. It defines a standard interface for UI components,
    ensuring that all drawable elements and event handlers are consistently managed across different implementations of the game UI.

    Attributes:
    - drawable_elements (list): A list of elements that can be drawn to the screen. These elements should implement a `draw` method.
    - event_handlers (list): A list of objects that can handle events. These objects should implement a `handle_event` method.
    """
    drawable_elements = []
    event_handlers = []

    # displays the board and the hud
    @abstractmethod
    def update(self, game_manager):
        """
        An abstract method that updates the UI components based on the game's current state. This method must be implemented
        by subclasses to ensure the UI reflects the latest game state.

        Parameters:
        - game_manager: An instance of the GameManager class, or similar, providing access to the game's current state
        and logic for updating UI components accordingly.
        """
        pass


class PygameUI(UI):
    """
    A concrete implementation of the UI class for a Pygame-based application. This class manages the game's graphical user interface, including drawing the game board and HUD, handling user inputs, and displaying menus.
    """

    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1300
    button_color = (0, 128, 255)
    button_highlight_color = (255, 255, 0)
    text_color = (255, 255, 255)

    def __init__(self, app) -> None:
        """
        Initializes the PygameUI with an application reference, sets up the screen, and initializes UI components like the HUD and game board.

        Parameters:
        - app: A reference to the main application object, used for callback notifications.
        """
        super().__init__()
        self.theme = pygame_menu.themes.THEME_DARK
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self._app = app
        self.start_button_clicked = False

        def start_game_cb(): return self._app.notify(self, "AiMakeMove")

        def undo_move_cb(): return self._app.notify(self, "UndoLastMove")

        def pause_game_cb(): return self._app.notify(self, "PauseGame")

        callbacks = (
            start_game_cb,
            undo_move_cb,
            pause_game_cb
        )
        hud = HUD(self, callbacks)

        def execute_move_cb(first_marble, second_marble, direction):
            return self._app.notify(self, "PlayerMakeMove", first_marble=first_marble,
                                    second_marble=second_marble, direction=direction)

        def marble_player_to_move_cb(marble_pos):
            return self._app.notify(self, "IsMarblePlayerToMove", marble_pos=marble_pos)

        def update_board_cb():
            return self.update(self._app.game_manager)

        callbacks = (
            execute_move_cb,
            marble_player_to_move_cb,
            update_board_cb
        )
        board = Board(callbacks)
        self.board = board
        self.hud = hud

        # add the drawables
        self.drawable_elements.append(board)
        self.drawable_elements.append(hud)

        # add the event handlers
        self.event_handlers.append(board)
        self.event_handlers.append(hud)

    def start_the_game(self, config):
        """
        Starts the game using the selected configuration.

        Parameters:
        - config: A dictionary containing the game configuration, such as player types, colors, and game rules.
        """
        self._app.notify(self, "StartGame", config=config)

    def run_game(self):
        """
        The main game loop. Handles events, updates the game state, and redraws the screen.
        """
        while True:
            for event in pygame.event.get():
                if event == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update(self._app.game_manager)

    def run(self):
        """
        Initializes Pygame and displays the main menu of the game.
        """
        pygame.init()
        self.main_menu()

    def update(self, game_manager):
        """
        Updates and redraws the game UI based on the current state of the game.

        Parameters:
        - game_manager: An instance of the game manager class that holds the current state of the game.
        """
        self.screen.fill((0, 0, 0))

        # update the score in the menu
        self.hud.white_balls, self.hud.black_balls = self._app.notify(
            self, "GetScore")

        for element in self.drawable_elements:
            element.draw(self.screen, game_manager)

        pygame.display.flip()

    @property
    def waiting_for_player_input(
        self): return self.board.waiting_for_player_input

    @waiting_for_player_input.setter
    def waiting_for_player_input(self, value):
        self.board.waiting_for_player_input = value

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
        player_color = menu.add.selector(
            'I Play As: ', [('Black', Marble.BLACK), ('White', Marble.WHITE)])  # Adding selector for player color

        cpu_level = menu.add.dropselect('Agent:     ', [
            ('Random moves', 1), ('Cameron', 2), ('Joey', 3), ('Elsa', 4), ('Callum', 5)], default=0,
            onchange=self.update_play_button)
        formation = menu.add.dropselect('Formation: ', [
            (f.name, f) for f in Formation], default=0, onchange=self.update_play_button)

        # Adding time limit and move limit selectors for both Black and White players
        black_time_limit = menu.add.dropselect('Black Time Limit: ', [
            ('1 min', 60), ('2 mins', 120), ('5 mins', 300), ('10 mins', 600)], default=0)
        black_move_limit = menu.add.dropselect('Black Move Limit: ', [
            ('10 moves', 10), ('20 moves', 20), ('50 moves', 50), ('Unlimited', None)], default=3)

        white_time_limit = menu.add.dropselect('White Time Limit: ', [
            ('1 min', 60), ('2 mins', 120), ('5 mins', 300), ('10 mins', 600)], default=0)
        white_move_limit = menu.add.dropselect('White Move Limit: ', [
            ('10 moves', 10), ('20 moves', 20), ('50 moves', 50), ('Unlimited', None)], default=3)

        menu.add.button('Play', lambda: self.start_the_game({
            'game_type': opponent_type.get_value(),
            'player_color': player_color.get_value(),
            'cpu_level': cpu_level.get_value(),
            'formation': formation.get_value(),
            'black_time_limit': black_time_limit.get_value(),
            'black_move_limit': black_move_limit.get_value(),
            'white_time_limit': white_time_limit.get_value(),
            'white_move_limit': white_move_limit.get_value()}))

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
        table.add_row(['Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        records = self._app.notify(self, "getRecordHistory")

        # Modify this to match formatting of record history
        for index, record in enumerate(records, start=1):
            str_record = str(record)
            table.add_row([str_record])
            print(record)

        menu.add.button('Back', self.run_game)
        menu.mainloop(self.screen)
