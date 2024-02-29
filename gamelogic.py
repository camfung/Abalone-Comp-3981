
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


class GameState:
    def __init__(self, board):
        self._board = board

    def get_state_space(self):
        pass

    def calc_white_move(self):
        pass

    def calc_black_move(self):
        pass
