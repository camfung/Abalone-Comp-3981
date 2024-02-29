
from enums import *
from records import RecordHistory
import csv
import abc
import copy


class Observable(abc.ABC):
    @abc.abstractmethod
    def join_room(self, player):
        pass

    @abc.abstractmethod
    def leave_room(self, player):
        pass

    @abc.abstractmethod
    def notify(self):
        pass


class GameManager(Observable):
    __instance = None

    @staticmethod
    def get_instance():
        if GameManager.__instance is None:
            GameManager.__instance = GameManager()
        return GameManager.__instance

    def __init__(self):
        if GameManager.__instance is not None:
            raise Exception("Only one instance of GameManager can be created")

        self._players = []
        GameManager.__instance = self

    def join_room(self, player):
        self._players.append(player)

    def leave_room(self, player):
        self._players.remove(player)

    def notify(self):
        pass

    def start_game(self):
        pass

    def stop_game(self):
        pass

    def pause_game(self):
        pass

    def undo_last_move(self):
        pass


class Game:
    id_counter = 0

    def __init__(self, formation):
        Game.id_counter += 1
        self._game_id = Game.id_counter
        self._current_game_state = Game.initialize_board_layout(formation)
        self._previous_game_state = copy.deepcopy(self._current_game_state)
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

    def set_move(self, player, move):
        pass


class GameState:
    def __init__(self, board, prev_game_state=None):
        self._board = board
        self._prev_game_state = prev_game_state

    def get_state_space(self):
        pass

    def calc_white_move(self):
        pass

    def calc_black_move(self):
        pass


