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
        starting_board = [[None, None, None, None,
                           None, None, None, None, None, None, None]]
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
                    raise InvalidMarbleValue(
                        f"{item} is not a valid marble value.")
            starting_board.append(formatted_row)

        file.close()

        starting_board.append(
            [None, None, None, None, None, None, None, None, None, None, None])
        return GameState(starting_board)

    def get_current_game_state(self):
        return self._current_game_state

    def set_move(self, player=None, move=None, timestamp=None):
        if player is None and move is None and timestamp is None:
            self._current_game_state = self._current_game_state.get_previous_game_state()
            self._record_history.remove_last_record()
            return

        next_marble = self._current_game_state.get_current_move_color()
        if next_marble is Marble.BLACK:
            next_marble = Marble.WHITE
        elif next_marble is Marble.WHITE:
            next_marble = Marble.BLACK
        else:
            raise InvalidMarbleValue("No Marble Value provided in Set Move.")

        new_board_state = self._current_game_state.generate_new_board_state(
            move)
        new_game_state = GameState(new_board_state,
                                   next_marble,
                                   copy.deepcopy(self._current_game_state))
        self._current_game_state = new_game_state
        self._record_history.add_record(move, player, timestamp)

    def get_record_history(self):
        return self._record_history

    def export_record_history(self):
        self._record_history.export_records()

    def set_game_state(self, new_game_state):
        self._current_game_state = new_game_state

    def __str__(self):
        game_state_str = str(self._current_game_state)
        return f"Game ID: {self._game_id}\n{game_state_str}"


class GameState:
    def __init__(self, board, marble=Marble.BLACK, prev_game_state=None):
        self._board = board
        self._current_move_color = marble
        self._white_balls = 14
        self._black_balls = 14
        self._prev_game_state = prev_game_state
        self._moves = self.__generate_possible_moves()

    def get_board(self):
        return self._board

    def get_current_move_color(self):
        return self._current_move_color

    def get_previous_game_state(self):
        return self._prev_game_state

    def get_possible_moves(self):
        return self._moves

    def __generate_possible_moves(self):
        moves = []
        row_col_modifiers = [(0, 1), (1, 0), (1, -1)]

        for row_index, row in enumerate(self._board):
            if row_index == 0 or row_index == len(self._board) - 1:
                continue

            for space_index, space in enumerate(row):
                if space_index == 0 or space_index == len(row) - 1:
                    continue

                if space is self._current_move_color:
                    for mod_index, (mod_row, mod_col) in enumerate(row_col_modifiers):
                        start_range = 0 if mod_row == 0 else 1

                        for group_size in range(start_range, 3):
                            first_ball_i = (row_index, space_index)
                            last_ball_i = (
                                row_index + group_size * mod_row, space_index + group_size * mod_col)

                            if self._board[last_ball_i[0]][last_ball_i[1]] is not self._current_move_color:
                                break

                            if not self.__check_inbounds(first_ball_i, last_ball_i, row):
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
        """
        Takes a given valid move and returns a new generated board state
        :param move: a move
        :precondition: move has been previously validated by check_move upon generation of move
        :return: a Marble 2D array representing the new board state
        """
        # Copy the Existing Board Value into the output variable
        new_board = copy.deepcopy(self._board)

        # Fetch Initial Ball Positions
        first_ball_i_x = move.get_pos_i()[0][0]
        first_ball_i_y = move.get_pos_i()[0][1]
        last_ball_i_x = move.get_pos_i()[1][0]
        last_ball_i_y = move.get_pos_i()[1][1]

        # Fetch Final Ball Positions
        first_ball_f_x = move.get_pos_f()[0][0]
        first_ball_f_y = move.get_pos_f()[0][1]
        last_ball_f_x = move.get_pos_f()[1][0]
        last_ball_f_y = move.get_pos_f()[1][1]

        # Fetch Middle Ball Positions
        remain_ball_i_x = first_ball_i_x
        remain_ball_i_y = first_ball_i_y
        if abs(first_ball_i_x - last_ball_i_x) > 1:
            remain_ball_i_x = (first_ball_i_x + last_ball_i_x) // 2

        if abs(first_ball_i_y - last_ball_i_y) > 1:
            remain_ball_i_y = (first_ball_i_y + last_ball_i_y) // 2

        remain_ball_f_x = first_ball_f_x
        remain_ball_f_y = first_ball_f_y
        if abs(first_ball_f_x - last_ball_f_x) > 1:
            remain_ball_f_x = (first_ball_f_x + last_ball_f_x) // 2

        if abs(first_ball_f_y - last_ball_f_y) > 1:
            remain_ball_f_y = (first_ball_f_y + last_ball_f_y) // 2

        # Move Subsequent Pieces in Same Direction
        if move.get_move_type() == MoveType.INLINE:
            # Declare Multipliers to Search for Subsequent Balls
            move_x = 1 if first_ball_f_x > first_ball_i_x else (
                -1 if first_ball_f_x < first_ball_i_x else 0)
            move_y = 1 if first_ball_f_y > first_ball_i_y else (
                -1 if first_ball_f_y < first_ball_i_y else 0)

            # Declare Variables for Initial and Final Ball Positions
            sub_ball_i_x = copy.copy(
                last_ball_i_x) if move_x > 0 else copy.copy(first_ball_i_x)
            sub_ball_i_y = copy.copy(
                last_ball_i_y) if move_y > 0 else copy.copy(first_ball_i_y)
            sub_ball_f_x = copy.copy(sub_ball_i_x)
            sub_ball_f_y = copy.copy(sub_ball_i_y)

            # Save Original Ball Positions to keep track when Tracing Backwards
            org_ball_x = copy.copy(sub_ball_i_x)
            org_ball_y = copy.copy(sub_ball_i_y)

            # Adjust Final Positions to Start Loop
            sub_ball_f_x += move_x
            sub_ball_f_y += move_y

            # Safety Lock Prevents Spaces from being shifted if there are no opposing pieces being pushed
            safety_lock = False
            if (new_board[sub_ball_f_x][sub_ball_f_y] is Marble.NONE
                    or new_board[sub_ball_f_x][sub_ball_f_y] is None):
                safety_lock = True

            # Search for the End of the Line
            while (new_board[sub_ball_f_x][sub_ball_f_y] is not Marble.NONE
                   and new_board[sub_ball_f_x][sub_ball_f_y] is not None):
                sub_ball_i_x += move_x
                sub_ball_f_x += move_x
                sub_ball_i_y += move_y
                sub_ball_f_y += move_y

            # Move Marbles to New Locations
            while ((sub_ball_i_x > org_ball_x and move_x > 0
                    or sub_ball_i_x < org_ball_x and move_x < 0
                    or sub_ball_i_x == org_ball_x and move_x == 0)
                   and
                   (sub_ball_i_y > org_ball_y and move_y > 0
                    or sub_ball_i_y < org_ball_y and move_y < 0
                    or sub_ball_i_y == org_ball_y and move_y == 0)
                   and not safety_lock):
                marble_color = copy.deepcopy(
                    new_board[sub_ball_i_x][sub_ball_i_y])
                new_board[sub_ball_i_x][sub_ball_i_y] = Marble.NONE

                # If the Marble is Off the Board, Delete it. Otherwise, Move Marble to Space
                if self._board[sub_ball_f_x][sub_ball_f_y] is not None:
                    new_board[sub_ball_f_x][sub_ball_f_y] = marble_color

                sub_ball_i_x -= move_x
                sub_ball_f_x -= move_x
                sub_ball_i_y -= move_y
                sub_ball_f_y -= move_y

        # Remove the all the Mover's marbles in the move
        new_board[first_ball_i_x][first_ball_i_y] = Marble.NONE
        new_board[last_ball_i_x][last_ball_i_y] = Marble.NONE
        new_board[remain_ball_i_x][remain_ball_i_y] = Marble.NONE

        # Place the Mover's marbles back on the board
        new_board[first_ball_f_x][first_ball_f_y] = move.get_marble()
        new_board[last_ball_f_x][last_ball_f_y] = move.get_marble()
        new_board[remain_ball_f_x][remain_ball_f_y] = move.get_marble()

        return new_board

    def __calc_move(self, **kwargs):
        move = Move(marble=self._current_move_color, **kwargs)
        if self.__check_move(move):
            return move
        return None

    @staticmethod
    def __check_move(move):
        return True

    def __check_inbounds(self, first_ball_i, last_ball_i, row):
        if first_ball_i[0] >= len(self._board) - 1 or first_ball_i[1] >= len(row) - 1:
            return False

        if last_ball_i[0] >= len(self._board) - 1 or last_ball_i[1] >= len(row) - 1:
            return False

        return True

    def __str__(self):
        # Hard-coded leading spaces for each row to match the desired output
        leading_spaces = ["", "        I   ", "       H   ", "      G   ", "    F   ",
                          "  E   ", "   D   ", "    C   ", "      B   ", "       A   ", "         """]
        board_str = ""

        for i, row in enumerate(self._board):
            row_str = leading_spaces[i]

            for index, space in enumerate(row):
                if space is None or space == "None":
                    continue
                elif space == Marble.WHITE:
                    row_str += "W  "
                elif space == Marble.BLACK:
                    row_str += "B  "
                elif space == Marble.NONE:
                    row_str += "-  "

            board_str += row_str.rstrip() + "\n"

        board_str += "          "
        for i in range(1, 6):
            board_str += f" {str(i)} "
        current_turn = "Black" if self._current_move_color == Marble.BLACK else "White"
        return f"Current Turn: {current_turn}\nBoard:\n{board_str}"


class Move:
    def __init__(self, first_ball_i, last_ball_i, direction, marble):
        self._direction = direction
        self._marble = marble
        self._pos_i = (first_ball_i, last_ball_i)
        self._pos_f = Move.__calc_pos_f(first_ball_i, last_ball_i, direction)
        self._selection_type = Move.__calc_selection_type(
            first_ball_i, last_ball_i)
        self._move_type = Move.__calc_move_type(
            first_ball_i, last_ball_i, direction, self._selection_type)

    @property
    def marble(self):
        return self._marble

    @staticmethod
    def __calc_pos_f(first_ball_i, last_ball_i, direction):
        if direction == Direction.UP_LEFT:
            position = ((first_ball_i[0] - 1, first_ball_i[1]),
                        (last_ball_i[0] - 1, last_ball_i[1]))
        elif direction == Direction.UP_RIGHT:
            position = ((first_ball_i[0] - 1, first_ball_i[1] + 1),
                        (last_ball_i[0] - 1, last_ball_i[1] + 1))
        elif direction == Direction.RIGHT:
            position = ((first_ball_i[0], first_ball_i[1] + 1),
                        (last_ball_i[0], last_ball_i[1] + 1))
        elif direction == Direction.DOWN_RIGHT:
            position = ((first_ball_i[0] + 1, first_ball_i[1]),
                        (last_ball_i[0] + 1, last_ball_i[1]))
        elif direction == Direction.DOWN_LEFT:
            position = ((first_ball_i[0] + 1, first_ball_i[1] - 1),
                        (last_ball_i[0] + 1, last_ball_i[1] - 1))
        elif direction == Direction.LEFT:
            position = ((first_ball_i[0], first_ball_i[1] - 1),
                        (last_ball_i[0], last_ball_i[1] - 1))
        else:
            raise InvalidDirection("Invalid direction passed to Move")

        return position

    @staticmethod
    def __calc_selection_type(first_ball_i, last_ball_i):
        # Return Horizontal if Rows are Same
        if first_ball_i[0] == last_ball_i[0]:
            return MarbleSelection.HORIZONTAL

        # Return Back-slash if Columns are Same
        if first_ball_i[1] == last_ball_i[1]:
            return MarbleSelection.BACKWARD_SLASH

        # Return Forward-slash if Rows and Columns are different
        return MarbleSelection.FORWARD_SLASH

    @staticmethod
    def __calc_move_type(first_ball_i, last_ball_i, direction, selection):
        # Return Single if First and Last Ball are the same
        if first_ball_i == last_ball_i:
            return MoveType.SINGLE

        # Return Inline if Horizontal Selection and Directions is Left or Right
        if (selection == MarbleSelection.HORIZONTAL
                and (Direction.LEFT == direction or Direction.RIGHT == direction)):
            return MoveType.INLINE

        # Return Inline if Selection is Backward Slash and Directions is UpLeft or DownRight
        if (selection == MarbleSelection.BACKWARD_SLASH
                and (Direction.UP_LEFT == direction or Direction.DOWN_RIGHT == direction)):
            return MoveType.INLINE

        # Return Inline if Selection is Forward Slash and Directions is UpRight or DownLeft
        if (selection == MarbleSelection.FORWARD_SLASH
                and (Direction.UP_RIGHT == direction or Direction.DOWN_LEFT == direction)):
            return MoveType.INLINE

        return MoveType.SIDE_STEP

    def get_pos_i(self):
        return self._pos_i

    def get_pos_f(self):
        return self._pos_f

    def get_direction(self):
        return self._direction

    def get_marble(self):
        return self._marble

    def get_selection_type(self):
        return self._selection_type

    def get_move_type(self):
        return self._move_type

    def __str__(self):
        if self._selection_type == MoveType.SINGLE:
            return (f"{chr(self._pos_i[0][0] + 64)}{self._pos_i[0][1]} "
                    f"-> {chr(self._pos_f[0][0] + 64)}{self._pos_f[0][1]}")
        return (f"{chr(self._pos_i[0][0] + 64)}{self._pos_i[0][1]},  "
                f"{chr(self._pos_i[1][0] + 64)}{self._pos_i[1][1]} "
                f"-> {chr(self._pos_f[0][0] + 64)}{self._pos_f[0][1]},  "
                f"{chr(self._pos_f[1][0] + 64)}{self._pos_f[1][1]}")
