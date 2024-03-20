import math
import threading
import time

import pygame_menu

from app.api.enums import Marble
from app.players.agent import AbaloneAgent
from app.ui.ui_components import Drawable, EventHandler


class HUD(Drawable, EventHandler):
    """
    A Heads-Up Display (HUD) class that handles the creation and management of the game's interface elements.
    It extends both Drawable and EventHandler interfaces to allow for drawing the HUD and handling input events.
    """
    HUD_HEIGHT = 200
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
        self.timer = None
        self.time_left_black = None
        self.time_left_white = None
        self._white_balls = 0
        self._black_balls = 0

        self._start_time_black = time.time()
        self._start_time_white = time.time()

        self._elapsed_time_black = 0
        self._elapsed_time_white = 0
        self._game_started = False

        self._black_check_time = True
        self._white_check_time = True

        self._turn_end = Marble.BLACK

        self.start_game_cb, self.undo_move_cb, self.pause_game_cb, self.update_score_cb = callbacks

# white move start time = time.time()
# time elapsed = time.time() - start time

# count down = 10 - time elapsed
    def update_hud_values(self, game_manager):
        if self._game_started:
            if game_manager.current_player_to_move == Marble.BLACK:
                if self._black_check_time:
                    self._start_time_black = time.time() - self._elapsed_time_black
                    self._black_check_time = False
                    self._white_check_time = True
                self._elapsed_time_black = time.time() - self._start_time_black
                self._turn_end = Marble.BLACK

                # updating the time left for black
                self.time_left_black.set_title(
                    f"Black Time Left: {self._elapsed_time_black:.2f}")
            elif game_manager.current_player_to_move == Marble.WHITE:
                if self._white_check_time:
                    self._start_time_white = time.time() - self._elapsed_time_white
                    self._white_check_time = False
                    self._black_check_time = True
                self._elapsed_time_white = time.time() - self._start_time_white
                self._turn_end = Marble.WHITE

                # updating the time left for white
                self.time_left_white.set_title(
                    f"White Time Left: {self._elapsed_time_white:.2f}")

            self.timer.set_title(
                f"Time: {self._elapsed_time_white:.2f}     Time: {self._elapsed_time_black:.2f}")
            # update the score
            self.white_balls, self.black_balls = self.update_score_cb()

    def start_game(self):
        self._game_started = True
        self._black_check_time = True
        self._white_check_time = True
        self.start_game_cb()

    def stop_game(self):
        self._elapsed_time_black = 0
        self._elapsed_time_white = 0
        self._game_started = False

        self._black_check_time = True
        self._white_check_time = True
        self.timer.set_title(
            f"Time: {self._elapsed_time_white:.2f}     Time: {self._elapsed_time_black:.2f}")
        self.ui_instance.play_menu()

    def restart_game(self):
        self._elapsed_time_black = 0
        self._elapsed_time_white = 0
        self._game_started = False

        self._black_check_time = True
        self._white_check_time = True
        self.timer.set_title(
            f"Time: {self._elapsed_time_white:.2f}     Time: {self._elapsed_time_black:.2f}")
        thread = threading.Thread(
            target=self.ui_instance.reset_board, args=(threading.current_thread(), ))
        thread.start()

    def pause_game(self):
        self._game_started = False
        self.pause_game_cb()

    def create_hud(self):
        """
        Creates the HUD menu with game control buttons like start, stop, pause, reset, undo last move,
        and show move history.

        Returns:
        - menu: A pygame_menu.Menu instance representing the HUD with all the control buttons.
        """
        menu = pygame_menu.Menu("Abalone", self.ui_instance.SCREEN_WIDTH, self.HUD_HEIGHT,
                                theme=self.theme, position=(0, 0, True), columns=5, rows=2)
        menu.add.button("Start Game", self.start_game,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Stop Game", self.stop_game,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Pause", self.pause_game,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Reset", self.restart_game,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Undo Last Move", self.undo_move_cb,
                        align=pygame_menu.locals.ALIGN_CENTER)
        menu.add.button("Show Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)

        self.score_label = menu.add.label(
            f"White: {self._white_balls}   Black:  {self._black_balls}  ")

        self.timer = menu.add.label(f"Time: {self._elapsed_time_white:.2f} Time: {self._elapsed_time_black:.2f}",
                                    selectable=False)
        self.time_left_white = menu.add.label(
            f"White Time Left: {self._elapsed_time_white:.2f}", selectable=False)
        self.time_left_black = menu.add.label(
            f"Black Time Left: {self._elapsed_time_black:.2f}", selectable=False)
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
                f"White Score: {self._white_balls}   Black Score: {self._black_balls}  ")

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

        self.update_hud_values(game_manager)
        menu = self.get_menu()
        menu.draw(surface)


class RecordMenu(Drawable, EventHandler):
    record_menu = None

    def __init__(self, gui):
        self.ui_instance = gui
        self.theme = self.ui_instance.theme

    # def create_record_menu(self):
    #     record_menu = pygame_menu.Menu(
    #         "Move History", 300, 850, theme=self.theme, position=(100, 100, True))
    #     table = record_menu.add.table(table_id='records_table',
    #                                   font_size=12, font_color="Black")
    #     table.default_cell_padding = 5
    #     table.default_row_background_color = 'white'
    #     table.add_row(['Moves'],
    #                   cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
    #
    #     records = self.ui_instance._app.notify(self, "getRecordHistory")
    #
    #     for index, record in enumerate(records, start=1):
    #         str_record = str(record)
    #         table.add_row([str_record])
    #         print(record)
    #
    #     record_menu.add.button('Back', self.ui_instance.display_move_history)  # for testing purposes
    #
    #     return record_menu
    #
    # def get_record_menu(self):
    #     if self.record_menu is None:
    #         self.record_menu = self.create_record_menu()
    #     return self.record_menu

    def handle_event(self, event):
        if self.record_menu is not None:
            self.record_menu.update([event])

    def get_agent_player(self):
        """
        Returns true if a given player is agent, for the purposes of displaying next agent move.
        If true, the agent player is black.
        :return: Boolean
        """
        return isinstance(self.ui_instance._app.players[0], AbaloneAgent)

    def draw(self, surface, game_manager):
        # Created here so that it updates
        record_menu = pygame_menu.Menu(
            "Move History", 300, 800, theme=self.theme, position=(100, 100, True))
        next_agent_move = record_menu.add.table(table_id='next_agent_move',
                                                font_size=12, font_color="Black")
        next_agent_move.default_cell_padding = 5
        next_agent_move.default_row_background_color = 'white'
        next_agent_move.add_row(['Next Agent Move'],
                                cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        black_table = record_menu.add.table(table_id='black_records_table',
                                            font_size=12, font_color="Black")
        black_table.default_cell_padding = 5
        black_table.default_row_background_color = 'white'
        black_table.add_row(['Black Moves'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        white_table = record_menu.add.table(table_id='white_records_table',
                                            font_size=12, font_color="Black")
        white_table.default_cell_padding = 5
        white_table.default_row_background_color = 'white'
        white_table.add_row(['White Moves'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        records = self.ui_instance._app.notify(self, "getRecordHistory")

        start_index = 1

        if records.get_records_length() > 15:
            record_menu.add.button('Show Full History',
                                   self.ui_instance.display_move_history)

            start_index = records.get_records_length(
            ) - math.ceil(records.get_records_length() / 2)

        for index, record in enumerate(records, start=1):
            str_record = str(record)
            if index >= start_index:
                if index % 2 == 0:
                    white_table.add_row([str_record])
                else:
                    black_table.add_row([str_record])

                if index == records.get_records_length() or index == records.get_records_length() - 1:
                    if self.get_agent_player() and index % 2 != 0:
                        next_agent_move.add_row([str_record])
                    elif not self.get_agent_player() and index % 2 == 0:
                        next_agent_move.add_row([str_record])

        self.record_menu = record_menu
        record_menu.draw(surface)
