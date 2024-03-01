
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
                if item in "None":
                    formatted_row.append(None)
                elif item in "WHITE":
                    formatted_row.append(Marble.WHITE)
                elif item in "BLACK":
                    formatted_row.append(Marble.BLACK)
                elif item in "EMPTY":
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

        next_marble = self._current_game_state.get_marble()
        if next_marble is Marble.BLACK:
            next_marble = Marble.WHITE
        elif next_marble is Marble.WHITE:
            next_marble = Marble.BLACK
        else:
            raise InvalidMarbleValue("No Marble Value provided in Set Move.")

        new_board_state = self._current_game_state.generate_new_board_state(move)
        new_game_state = GameState(new_board_state,
                                   next_marble,
                                   copy.deepcopy(self._current_game_state))
        self._current_game_state = new_game_state

    def get_record_history(self):
        return self._record_history

    def export_record_history(self):
        self._record_history.export_records()


class GameState:
    def __init__(self, board, marble=Marble.BLACK, prev_game_state=None):
        self._board = board
        self._marble = marble
        self._prev_game_state = prev_game_state
        self._moves = self.__generate_possible_moves()

    def get_board(self):
        return self._board

    def get_marble(self):
        return self._marble

    def get_previous_game_state(self):
        return self._prev_game_state

    def get_possible_moves(self):
        return self._moves

    def __generate_possible_moves(self):
        moves = []

        for row_index, row in enumerate(self._board):
            if row_index == 0 or row_index == len(self._board) - 1:
                continue

            for space_index, space in enumerate(row):
                if space_index == 0 or space_index == len(row) - 1:
                    continue

                if space is self._marble:
                    # Select Groupings - Right
                    for group_size in range(0, 3):
                        first_ball_i = (row_index, space_index)
                        last_ball_i = (row_index, space_index + group_size)

                        if self._board[last_ball_i[0]][last_ball_i[1]] is not self._marble:
                            break

                        if self.__check_groupings(first_ball_i, last_ball_i, row):
                            continue

                        for direction in Direction:
                            move = self.__calc_move(first_ball_i=first_ball_i,
                                                    last_ball_i=last_ball_i,
                                                    direction=direction)
                            if move is not None:
                                moves.append(move)

                    # Select Groupings X Direction - DownRight
                    for group_size in range(0, 3):
                        first_ball_i = (row_index, space_index)
                        last_ball_i = (row_index + group_size, space_index)

                        if self._board[last_ball_i[0]][last_ball_i[1]] is not self._marble:
                            break

                        if self.__check_groupings(first_ball_i, last_ball_i, row):
                            continue

                        for direction in Direction:
                            move = self.__calc_move(first_ball_i=first_ball_i,
                                                    last_ball_i=last_ball_i,
                                                    direction=direction)
                            if move is not None:
                                moves.append(move)

                    # Select Groupings X Direction - DownLeft
                    for group_size in range(0, 3):
                        first_ball_i = (row_index, space_index)
                        last_ball_i = (row_index + group_size, space_index - group_size)

                        if self._board[last_ball_i[0]][last_ball_i[1]] is not self._marble:
                            break

                        if self.__check_groupings(first_ball_i, last_ball_i, row):
                            continue

                        for direction in Direction:
                            move = self.__calc_move(first_ball_i=first_ball_i,
                                                    last_ball_i=last_ball_i,
                                                    direction=direction)
                            if move is not None:
                                moves.append(move)

        return moves

    def convert_moves_to_game_states(self):
        game_states = []

        for move in self._moves:
            new_game_state = self.generate_new_board_state(move)
            game_states.append(new_game_state)

        return game_states

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
        remain_ball_i_x = first_ball_i_x
        remain_ball_i_y = first_ball_i_y
        if first_ball_i_x - last_ball_i_x > 1:
            remain_ball_i_x = (first_ball_i_x + last_ball_i_x) / 2

        if first_ball_i_y - last_ball_i_y > 1:
            remain_ball_i_y = (first_ball_i_y + last_ball_i_y) / 2

        remain_ball_f_x = first_ball_i_x
        remain_ball_f_y = first_ball_i_y
        if first_ball_f_x - last_ball_i_x > 1:
            remain_ball_f_x = (first_ball_i_x + last_ball_i_x) / 2

        if first_ball_i_y - last_ball_i_y > 1:
            remain_ball_f_y = (first_ball_i_y + last_ball_i_y) / 2

        new_board[remain_ball_i_x][remain_ball_i_y] = Marble.NONE
        new_board[remain_ball_f_x][remain_ball_f_y] = move.get_marble()

        return new_board

    def __calc_move(self, **kwargs):
        move = Move(self._marble, **kwargs)
        if self.__check_move(move):
            return move
        return None

    @staticmethod
    def __check_move(move):
        return True

    def __check_groupings(self, first_ball_i, last_ball_i, row):
        if first_ball_i[0] >= len(self._board) - 1 or first_ball_i[1] >= len(row) - 1:
            return False

        if last_ball_i[0] >= len(self._board) - 1 or last_ball_i[1] >= len(row) - 1:
            return False

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
