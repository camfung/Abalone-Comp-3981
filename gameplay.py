
import copy
from enums import *
from records import RecordHistory
from exceptions import InvalidMarbleValue, InvalidDirection
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
                    raise InvalidMarbleValue(f"{item} is not a valid marble value.")
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
            return

        new_board_state = self._current_game_state.generate_new_board_state(move)
        new_game_state = GameState(new_board_state, copy.deepcopy(self._current_game_state))
        self._current_game_state = new_game_state

    def get_record_history(self):
        return self._record_history

    def export_record_history(self):
        self._record_history.export_records()


class GameState:
    def __init__(self, board, prev_game_state=None):
        self._board = board
        self._prev_game_state = prev_game_state

    def get_board(self):
        return self._board

    def get_previous_game_state(self):
        return self._prev_game_state

    def get_state_space(self, marble):
        moves = []
        for row in self._board:
            for space in row:
                if space is marble:
                    for direction in Direction:
                        # Select Groupings X Direction
                        for x in range(0, 4):
                            first_ball_i = (self._board(row), row.index(space))
                            last_ball_i = (self._board(row) + x, row.index(space))
                            move = self.__calc_move(marble,
                                                    first_ball_i=first_ball_i,
                                                    last_ball_i=last_ball_i,
                                                    direction=direction,
                                                    marble=marble)
                            if move is not None:
                                moves.append(move)
        return moves

    def generate_new_board_state(self, move):
        # Copy the Existing Board Value into the output variable
        new_board = copy.deepcopy(self._board)

        # Move the First and Last Balls
        first_ball_i_x = move.get_pos_i()[0][0]
        first_ball_i_y = move.get_pos_i()[0][1]
        last_ball_i_x = move.get_pos_i()[1][0]
        last_ball_i_y = move.get_pos_i()[1][1]
        new_board[first_ball_i_x][first_ball_i_y] = Marble.NONE
        new_board[last_ball_i_x][last_ball_i_y] = Marble.NONE

        first_ball_f_x = move.get_pos_f()[0][0]
        first_ball_f_y = move.get_pos_f()[0][1]
        last_ball_f_x = move.get_pos_f()[1][0]
        last_ball_f_y = move.get_pos_f()[1][1]
        new_board[first_ball_f_x][first_ball_f_y] = move.get_marble()
        new_board[last_ball_f_x][last_ball_f_y] = move.get_marble()

        # Move any remaining Balls
        if move.get_pos_i()[0][1] - move.get_pos_i()[0][0] > 1:
            pass

        return new_board

    def __calc_move(self, marble, **kwargs):
        move = Move(marble, **kwargs)
        if self.__check_move(move):
            return move
        return None

    @staticmethod
    def __check_move(move):
        return True


class Move:
    def __init__(self, first_ball_i, last_ball_i, direction, marble):
        self._direction = direction
        self._marble = marble
        self._pos_i = (first_ball_i, last_ball_i)
        self._pos_f = Move.__calc_pos_f(direction, first_ball_i, last_ball_i)

    @staticmethod
    def __calc_pos_f(first_ball_i, last_ball_i, direction):
        position = None

        if direction == Direction.UP_LEFT:
            position = ((first_ball_i[0] - 1, first_ball_i[1]), (last_ball_i[0] - 1, last_ball_i[1]))
        elif direction == Direction.UP_RIGHT:
            position = ((first_ball_i[0] - 1, first_ball_i[1] + 1), (last_ball_i[0] - 1, last_ball_i[1] + 1))
        elif direction == Direction.RIGHT:
            position = ((first_ball_i[0], first_ball_i[1] + 1), (last_ball_i[0], last_ball_i[1] + 1))
        elif direction == Direction.DOWN_RIGHT:
            position = ((first_ball_i[0] + 1, first_ball_i[1]), (last_ball_i[0] + 1, last_ball_i[1]))
        elif direction == Direction.DOWN_LEFT:
            position = ((first_ball_i[0] + 1, first_ball_i[1] - 1), (last_ball_i[0] + 1, last_ball_i[1] - 1))
        elif direction == Direction.LEFT:
            position = ((first_ball_i[0], first_ball_i[1] - 1), (last_ball_i[0], last_ball_i[1] - 1))
        else:
            raise InvalidDirection("Invalid direction passed to Move")

        return position

    def get_pos_i(self):
        return self._pos_i

    def get_pos_f(self):
        return self._pos_f

    def get_direction(self):
        return self._direction

    def get_marble(self):
        return self._marble

    def __str__(self):
        return f"{self._pos_i} -> {self._pos_f}"
