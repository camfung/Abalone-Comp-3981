
from enums import *
from records import RecordHistory
import csv


class Game:
    id_counter = 0

    def __init__(self, formation):
        Game.id_counter += 1
        self._game_id = Game.id_counter
        self._current_game_state = Game.initialize_board_layout(formation)
        self._record_history = RecordHistory(self._game_id)

    @staticmethod
    def initialize_board_layout(formation):
        starting_board = [[None, None, None, None, None, None, None, None, None, None, None]]
        file = None
        csv_reader = None

        if formation == Formation.DEFAULT:
            file = open('./formations/default.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        elif formation == Formation.BELGIAN_DAISY:
            file = open('./formations/belgian_daisy.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        elif formation == Formation.GERMAN_DAISY:
            file = open('./formations/german_daisy.csv', 'r')
            csv_reader = csv.reader(file, delimiter=',')

        for row in csv_reader:
            formatted_row = []
            for item in row:
                if item == "None":
                    formatted_row.append(None)
                elif item == "Marble.White":
                    formatted_row.append(Marble.WHITE)
                elif item == "Marble.Black":
                    formatted_row.append(Marble.BLACK)
                elif item == "Marble.None":
                    formatted_row.append(Marble.NONE)
                else:
                    raise Exception("Invalid Value")
            starting_board.append(formatted_row)

        file.close()

        starting_board.append([None, None, None, None, None, None, None, None, None, None, None])
        return GameState(starting_board)

    def get_current_game_state(self):
        return self._current_game_state

    def set_move(self, player=None, move=None):
        if player is None and move is None:
            self._current_game_state = self._current_game_state.get_previous_game_state()
            self._record_history.remove_last_record()

    def get_record_history(self):
        return self._record_history


class GameState:
    def __init__(self, board, prev_game_state=None):
        self._board = board
        self._prev_game_state = prev_game_state

    def get_board(self):
        return self._board

    def get_previous_game_state(self):
        return self._prev_game_state

    def get_state_space(self):
        pass

    def calc_move(self, marble):
        pass

    def set_board(self, marble, move):
        pass


class Move:
    def __init__(self, first_ball_i, last_ball_i, first_ball_f, last_ball_f, direction, player):
        self._pos_i = (first_ball_i, last_ball_i)
        self._pos_f = (first_ball_f, last_ball_f)
        self._direction = direction
        self._player = player

    def get_pos_i(self):
        return self._pos_i

    def get_pos_f(self):
        return self._pos_f

    def get_direction(self):
        return self._direction

    def get_player(self):
        return self._player

    def __str__(self):
        return f"{self._pos_i} -> {self._pos_f}"
