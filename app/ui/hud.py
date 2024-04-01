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
        self.time_left_black_label = None
        self.time_left_white_label = None
        self.timer = None
        self._white_balls = 0
        self._black_balls = 0

        self.start_game_cb, self.undo_move_cb, self.pause_game_cb, self.update_score_cb, self.start_timer_cb, self.reset_timer_cb, self.get_timer_values_cb = callbacks

    # white move start time = time.time()
    # time elapsed = time.time() - start time

    # count down = 10 - time elapsed
    def update_hud_values(self, game_manager):
        current_turn_start_time, black_total_aggregate_time, white_total_aggregate_time, white_turn_time_limit, black_turn_time_limit = self.get_timer_values_cb()
        # updating the time left for black
        if game_manager.current_player_to_move == Marble.BLACK:
            self.time_left_black_label.set_title(
                f"Black Time Left: {black_turn_time_limit - current_turn_start_time:.2f}")
            self.time_left_white_label.set_title(
                f"White Time Left: {white_turn_time_limit:.2f}")
        # updating the time left for white
        elif game_manager.current_player_to_move == Marble.WHITE:
            self.time_left_white_label.set_title(
                f"White Time Left: {white_turn_time_limit - current_turn_start_time:.2f}")
            self.time_left_black_label.set_title(
                f"Black Time Left: {black_turn_time_limit:.2f}")

        self.timer.set_title(
            f"Time: {white_total_aggregate_time:.2f}     Time: {black_total_aggregate_time:.2f}")
        # update the score
        self.white_balls, self.black_balls = self.update_score_cb()

    def start_game(self):
        self.start_timer_cb()
        self.start_game_cb()

    def stop_game(self):
        self.reset_timer_cb()
        _, aggregate_time_black, aggregate_time_white, _, _ = self.get_timer_values_cb()
        self.timer.set_title(
            f"Time: {aggregate_time_white:.2f}     Time: {aggregate_time_black:.2f}")
        self.ui_instance.play_menu()

    def restart_game(self):
        self.reset_timer_cb()
        _, aggregate_time_black, aggregate_time_white, _, _ = self.get_timer_values_cb()
        self.timer.set_title(
            f"Time: {aggregate_time_white:.2f}     Time: {aggregate_time_black:.2f}")
        thread = threading.Thread(
            target=self.ui_instance.reset_board, args=(threading.current_thread(),))
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
        _, aggregate_time_black, aggregate_time_white, _, _ = self.get_timer_values_cb()

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
        menu.add.button("Show Full Move History", self.ui_instance.display_move_history,
                        align=pygame_menu.locals.ALIGN_CENTER)

        self.score_label = menu.add.label(
            f"White: {self._white_balls}   Black:  {self._black_balls}  ")

        self.timer = menu.add.label(f"Time: {aggregate_time_white:.2f} Time: {aggregate_time_black:.2f}",
                                    selectable=False)
        self.time_left_white_label = menu.add.label(
            f"White Time Left: {aggregate_time_white:.2f}", selectable=False)
        self.time_left_black_label = menu.add.label(
            f"Black Time Left: {aggregate_time_black:.2f}", selectable=False)
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

        menu = self.get_menu()
        self.update_hud_values(game_manager)
        menu.draw(surface)


class RecordMenu(Drawable, EventHandler):
    record_menu = None

    def __init__(self, gui, moves_left_cb, pause_game_cb):
        self.ui_instance = gui
        self.theme = self.ui_instance.theme
        self.moves_left_cb = moves_left_cb
        self.pause_game_cb = pause_game_cb

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

    def show_full_history(self):
        self.pause_game_cb()
        self.ui_instance.display_move_history()

    def draw(self, surface, game_manager):
        ##Moved records length to the top to position move left label
        records = self.ui_instance._app.notify(self, "getRecordHistory")

        start_index = 1

        record_len = records.get_records_length()

        ##Logic to position the move left label
        if record_len > 15:
            start_index = record_len - math.ceil(record_len / 2)
            if record_len % 2 == 1:
                move_left_size = record_len - start_index - 1
            else:
                move_left_size = record_len - start_index
        else:
            if record_len % 2 == 1:
                move_left_size = record_len - 1
            else:
                move_left_size = record_len
        # Created here so that it updates
        record_menu = pygame_menu.Menu(
            "Move History", 450, 800, theme=self.theme, position=(100, 100, True))

        record_menu.add.label(f"Moves left: {self.moves_left_cb()}", align=pygame_menu.locals.ALIGN_CENTER, selectable=False).translate(0, -(300-13*move_left_size))

        next_agent_move = record_menu.add.table(table_id='next_agent_move',
                                                font_size=12, font_color="Black")
        next_agent_move.default_cell_padding = 5
        next_agent_move.default_row_background_color = 'white'
        next_agent_move.add_row(['Next Agent Move'],
                                cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        table = record_menu.add.table(table_id='black_records_table',
                                      font_size=12, font_color="Black")
        table.default_cell_padding = 5
        table.default_row_background_color = 'white'
        table.add_row(['Black Moves', 'White Moves'],
                      cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        # black_table = record_menu.add.table(table_id='black_records_table',
        #                                     font_size=12, font_color="Black")
        # black_table.default_cell_padding = 5
        # black_table.default_row_background_color = 'white'
        # black_table.add_row(['Black Moves'],
        #                     cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
        #
        # white_table = record_menu.add.table(table_id='white_records_table',
        #                                     font_size=12, font_color="Black")
        # white_table.default_cell_padding = 5
        # white_table.default_row_background_color = 'white'
        # white_table.add_row(['White Moves'],
        #                     cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

        if record_len > 15:
            record_menu.add.button('Show Full History',
                                   self.show_full_history)
            start_index = record_len - math.ceil(record_len / 2)

        for i in range(start_index - 1, record_len, 2):
            try:
                black_move = str(records.get_record(
                    i).condensed_str()) if i < record_len else ''
                white_move = str(records.get_record(
                    i + 1).condensed_str()) if i + 1 < record_len else ''
                table.add_row([black_move, white_move])
            except IndexError as e:
                pass

        for index, record in enumerate(records, start=1):
            str_record = str(record)

            if index >= start_index:
                # if index % 2 == 0:
                #     white_table.add_row([str_record])
                # else:
                #     black_table.add_row([str_record])

                if index == records.get_records_length() or index == records.get_records_length() - 1:
                    if self.get_agent_player() and index % 2 != 0:
                        next_agent_move.add_row([str_record])
                    elif not self.get_agent_player() and index % 2 == 0:
                        next_agent_move.add_row([str_record])

        self.record_menu = record_menu
        record_menu.draw(surface)
