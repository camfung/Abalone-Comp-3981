import time

from app.api.enums import Marble
from app.communication.game_manager import GameManager


class Timer:

    def __init__(self):
        self._black_total_aggregate_time = 0
        self._white_total_aggregate_time = 0

        self.current_turn_start_time = 0
        self._elapsed_time = 0
        self._white_turn_time_limit = 0
        self._black_turn_time_limit = 0

        self._start_time_black = time.time()
        self._start_time_white = time.time()

        self._game_started = False

        self._black_start_turn = True
        self._white_start_turn = True

        self._is_paused = False
        self._pause_start_time_black = 0
        self._pause_start_time_white = 0

    def start_timer(self):
        self._game_started = True
        self._black_check_time = True
        self._white_check_time = True

    def reset_time(self):
        self._game_started = False
        self._black_total_aggregate_time = 0
        self._white_total_aggregate_time = 0

        self._black_start_turn = True
        self._white_start_turn = True

    def get_timer_values(self):
        return (self._elapsed_time - self.current_turn_start_time, self._black_total_aggregate_time, self._white_total_aggregate_time, self._white_turn_time_limit,
                self._black_turn_time_limit)

    def update_timer(self, game_manager):
        if self._game_started and not self._is_paused:
            self._elapsed_time = time.time()
            if game_manager.current_player_to_move == Marble.BLACK:
                if self._black_start_turn:
                    self._start_time_black = time.time() - self._black_total_aggregate_time
                    self._black_start_turn = False
                    self._white_start_turn = True
                self._black_total_aggregate_time = time.time() - self._start_time_black

            elif game_manager.current_player_to_move == Marble.WHITE:
                if self._white_start_turn:
                    self._start_time_white = time.time() - self._white_total_aggregate_time
                    self._white_start_turn = False
                    self._black_start_turn = True
                self._white_total_aggregate_time = time.time() - self._start_time_white

    def set_current_turn_start_time(self):
        self.current_turn_start_time = time.time()

    def pause(self, game_manager: GameManager):
        if self._is_paused is not True:
            if game_manager.current_player_to_move == Marble.BLACK:
                self._pause_start_time_black = time.time()
            elif game_manager.current_player_to_move == Marble.WHITE:
                self._pause_start_time_white = time.time()
        else:
            if game_manager.current_player_to_move == Marble.BLACK:
                pass
            elif game_manager.current_player_to_move == Marble.WHITE:
                pass

        self._is_paused = not self._is_paused
