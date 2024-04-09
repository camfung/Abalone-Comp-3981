import time

from app.api.enums import Marble


class Timer:

    def __init__(self):
        self._white_check_time = None
        self._black_check_time = None
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
        if not self.paused:
            self.current_turn_start_time = time.time()
            self._elapsed_time = time.time()
        self._game_started = True
        self._black_check_time = True
        self._white_check_time = True

    def reset_time(self):
        self.paused = False
        self._game_started = False
        self._black_total_aggregate_time = 0
        self._white_total_aggregate_time = 0

        self._black_start_turn = True
        self._white_start_turn = True

    def get_timer_values(self):
        return (
            self._elapsed_time - self.current_turn_start_time,
            self._black_total_aggregate_time,
            self._white_total_aggregate_time,
            self._white_turn_time_limit,
            self._black_turn_time_limit
        )

    def pause_timer(self):
        self.paused = True
        self._game_started = False
        self._black_start_turn = True
        self._white_start_turn = True

    def undo_move(self):
        self.paused = False
        self._game_started = False
        self._black_start_turn = True
        self._white_start_turn = True


    def update_timer(self, game_manager):
        if self._game_started:
            if game_manager._app.players[0].num_balls < 9 or game_manager._app.players[1].num_balls < 9:
                self.pause_timer()

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


    def get_white_aggregate_time(self):
        return self._white_total_aggregate_time

    def get_black_aggregate_time(self):
        return self._black_total_aggregate_time

    @property
    def game_started(self):
        return self._game_started

