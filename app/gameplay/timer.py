import time

from app.api.enums import Marble


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

        self.paused = False

    def start_timer(self):
        self._game_started = True
        self.paused = False
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

    def pause_timer(self):
        self.paused = True
        self._game_started = False
        self._black_start_turn = True
        self._white_start_turn = True


    def update_timer(self, game_manager):
        if self._game_started:
            if game_manager.current_player_to_move == Marble.BLACK:
                if self._black_start_turn:
                    self.current_turn_start_time = time.time() - (self._elapsed_time - self.current_turn_start_time)
                    self._start_time_black = time.time() - self._black_total_aggregate_time
                    self._black_start_turn = False
                    self._white_start_turn = True
                self._black_total_aggregate_time = time.time() - self._start_time_black

            elif game_manager.current_player_to_move == Marble.WHITE:
                if self._white_start_turn:
                    self.current_turn_start_time = time.time() - (self._elapsed_time - self.current_turn_start_time)
                    self._start_time_white = time.time() - self._white_total_aggregate_time
                    self._white_start_turn = False
                    self._black_start_turn = True
                self._white_total_aggregate_time = time.time() - self._start_time_white
            self._elapsed_time = time.time()

    def set_current_turn_start_time(self):
        self.current_turn_start_time = time.time()

