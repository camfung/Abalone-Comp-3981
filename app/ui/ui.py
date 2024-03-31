
from abc import ABC, abstractmethod
import sys
import pygame
from app.api.enums import GameType, Marble, AgentType
import pygame_menu
from app.api.enums import Formation
from app.ui.board import Board
from app.ui.hud import HUD, RecordMenu


class UI(ABC):
    """
    An abstract base class representing the user interface (UI) of the game.
    It defines a standard interface for UI components,
    ensuring that all drawable elements and event handlers are consistently managed
    across different implementations of the game UI.

    Attributes:
    - drawable_elements (list): A list of elements that can be drawn to the screen.
    These elements should implement a `draw` method.
    - event_handlers (list): A list of objects that can handle events.
    These objects should implement a `handle_event` method.
    """
    drawable_elements = []
    event_handlers = []

    # displays the board and the hud
    @abstractmethod
    def update(self, game_manager):
        """
        An abstract method that updates the UI components based on the game's current state.
        This method must be implemented
        by subclasses to ensure the UI reflects the latest game state.

        Parameters:
        - game_manager: An instance of the GameManager class, or similar, providing access to the game's current state
        and logic for updating UI components accordingly.
        """
        pass


class PygameUI(UI):
    """
    A concrete implementation of the UI class for a Pygame-based application.
    This class manages the game's graphical user interface,
    including drawing the game board and HUD, handling user inputs, and displaying menus.
    """

    SCREEN_HEIGHT = 1000
    SCREEN_WIDTH = 1450
    button_color = (0, 128, 255)
    button_highlight_color = (255, 255, 0)
    text_color = (255, 255, 255)

    def __init__(self, app) -> None:
        """
        Initializes the PygameUI with an application reference, sets up the screen,
        and initializes UI components like the HUD and game board.

        Parameters:
        - app: A reference to the main application object, used for callback notifications.
        """
        super().__init__()
        iconSurface = pygame.image.load('app/images/icon.png')
        pygame.display.set_icon(iconSurface)
        self.theme = pygame_menu.themes.THEME_DARK
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self._app = app
        self.start_button_clicked = False

        def start_game_cb(): return self._app.notify(self, "AiMakeMove")

        def undo_move_cb(): return self._app.notify(self, "UndoLastMove")

        def pause_game_cb(): return self._app.notify(self, "PauseTimer")

        def update_score_cb(): return self._app.notify(self, "GetScore")

        def start_timer_cb():
            return self._app.notify(self, "StartTimer")

        def reset_timer_cb():
            return self._app.notify(self, "ResetTimer")

        def get_timer_values_cb():
            return self._app.notify(self, "GetTimerValues")

        callbacks = (
            start_game_cb,
            undo_move_cb,
            pause_game_cb,
            update_score_cb,
            start_timer_cb,
            reset_timer_cb,
            get_timer_values_cb
        )
        hud = HUD(self, callbacks)
        record_menu = RecordMenu(self)

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
        self.record_menu = record_menu

        # add the drawables
        self.drawable_elements.append(board)
        self.drawable_elements.append(hud)
        self.drawable_elements.append(record_menu)

        # add the event handlers
        self.event_handlers.append(board)
        self.event_handlers.append(hud)
        self.event_handlers.append(record_menu)

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

        self._app.notify(self, "UpdateTimer")

        # update the score in the menu
        self.hud.white_balls, self.hud.black_balls = self._app.notify(
            self, "GetScore")

        for element in self.drawable_elements:
            element.draw(self.screen, game_manager)

        if self.hud.white_balls < 9 or self.hud.black_balls < 9:
            self.draw_game_victory()
            self._app.notify(self, "PauseTimer")

        pygame.display.flip()

    def draw_game_victory(self):
        winner = "White" if self.hud.white_balls > self.hud.black_balls else "Black"
        game_over_text = pygame.font.Font(None, 100).render(
            f"{winner} wins!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(self.SCREEN_WIDTH // 3, 500))

        background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20,
                                      text_rect.height + 20)
        pygame.draw.rect(self.screen, (0, 0, 0), background_rect)
        self.screen.blit(game_over_text, text_rect)

    def reset_board(self, thread):
        self._app.reset_board()
        thread.join()

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
            'Opponent: ', [('Agent', GameType.PLAYER_VS_AGENT), ('Human', GameType.PLAYER_VS_PLAYER)])
        player_color = menu.add.selector(
            'I Play As: ', [('Black', Marble.BLACK), ('White', Marble.WHITE)])  # Adding selector for player color

        agent_level = menu.add.dropselect('Agent:     ', [('Cameron', AgentType.AGENT_CAMERON),
                                                          ('Default', AgentType.ABALONE_AGENT), (
                                                              'Random Moves', AgentType.RANDOM_AGENT),
                                                          ('Joey',
                                                           AgentType.AGENT_JOEY),
                                                          ('Elsa', AgentType.AGENT_ELSA), ('Callum', AgentType.AGENT_CALLUM)],
                                          default=0, onchange=self.update_play_button)
        formation = menu.add.dropselect('Formation: ', [
            (f.name, f) for f in Formation], default=0, onchange=self.update_play_button)

        # Adding time limit and move limit selectors for both Black and White players
        black_time_limit = menu.add.text_input(
            'Black Time Limit (Seconds): ', default=30, input_type=pygame_menu.locals.INPUT_INT, maxchar=4)

        white_time_limit = menu.add.text_input(
            'White Time Limit (Seconds): ', default=30, input_type=pygame_menu.locals.INPUT_INT, maxchar=4)

        move_limit = menu.add.text_input(
            'Move Limit: ', default=20, input_type=pygame_menu.locals.INPUT_INT, maxchar=3)

        menu.add.button('Play', lambda: self.start_the_game({
            'game_type': opponent_type.get_value(),
            'player_color': player_color.get_value(),
            'agent_level': agent_level.get_value(),
            'formation': formation.get_value(),
            'black_time_limit': black_time_limit.get_value(),
            'move_limit': move_limit.get_value(),
            'white_time_limit': white_time_limit.get_value()}))

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
                               font_size=18, font_color="Black")
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Black Moves', 'White Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        records = self._app.notify(self, "getRecordHistory")
        record_len = records.get_records_length()

        for i in range(0, record_len, 2):
            black_move = str(records.get_record(i)) if i < record_len else ''
            white_move = str(records.get_record(i + 1)) if i + \
                1 < record_len else ''
            table.add_row([black_move, white_move])

        menu.add.button('Back', self.run_game)
        menu.mainloop(self.screen)
