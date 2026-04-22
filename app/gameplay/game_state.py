import copy
from typing import List

from app.api.exceptions import InvalidMarbleValue
from app.gameplay.move import Move
from app.api.enums import *


class GameState:
    """
    Represents the state of the game at a particular moment,
    including the board configuration and the current player's turn.
    """

    def __init__(self, board, move=None, marble=Marble.BLACK, prev_game_state=None):
        """
        Initializes a new game state.

        Parameters:
        - board: The board configuration as a 2D list.
        - marble: The current player's marble color.
        - prev_game_state: The previous game state, if any.
        """
        self._board = board
        self._move = move
        self._current_move_color = marble
        self._prev_game_state = prev_game_state
        self._white_balls, self._black_balls = self.get_ball_count()

    def get_board(self):
        return self._board

    def get_current_move_color(self):
        return self._current_move_color

    def get_previous_game_state(self):
        return self._prev_game_state

    def get_move(self):
        """
        Get Move that made up the current game state
        :return: Move
        """
        return self._move

    def get_ball_count(self):
        """
        Get Ball Count of Board
        :return: white_ball_count (int), black_ball_count (int)
        """
        white_count = 0
        black_count = 0
        for row in self._board:
            for col in row:
                if col == Marble.BLACK:
                    black_count += 1
                elif col == Marble.WHITE:
                    white_count += 1
        return white_count, black_count

    @property
    def white_balls(self):
        return self._white_balls

    @property
    def black_balls(self):
        return self._black_balls

    def line_to_edge(self, from_space: tuple, direction: Direction):
        # check if from_space is on the board
        if (from_space[0] < 1 or from_space[0] >= len(self._board) - 1
                or from_space[1] < 1 or from_space[1] >= len(self._board[0]) - 1):
            raise InvalidMarbleValue("The space is not on the board")
        line = [from_space]
        while self.get_marble(line[-1]) is not None:
            neighbor = self.get_neighbor(line[-1], direction)
            line.append(neighbor)
        line.pop()
        return line

    def get_neighbor(self, pos, direction):
        """
        Get the neighbor of a position in a given direction
        :param pos: The position of the marble
        :param direction: The direction to check
        :return: The position of the neighbor
        """
        row, col = pos
        # check if it is in bounds
        if row < 1 or row >= len(self._board)-1 or col < 1 or col >= len(self._board[0])-1:
            return None
        if direction == Direction.UP_LEFT:
            return row - 1, col
        elif direction == Direction.UP_RIGHT:
            return row - 1, col + 1
        elif direction == Direction.RIGHT:
            return row, col + 1
        elif direction == Direction.DOWN_RIGHT:
            return row + 1, col
        elif direction == Direction.DOWN_LEFT:
            return row + 1, col - 1
        elif direction == Direction.LEFT:
            return row, col - 1

    def get_marble(self, pos):
        """
        Get the marble at a given position
        :param pos: The Marble position
        :return: The Marble color at the position
        """
        return self._board[pos[0]][pos[1]]

    def generate_own_marble_lines(self):
        """
        Generates all adjacent straight lines with up to three marbles of the player whose turn it is.

        This method iterates over all the spaces on the board. For each space that contains a marble of the
        current player, it yields that space as a potential move. Then, it checks for adjacent marbles in specific
        directions (NORTH_WEST, NORTH_EAST, and EAST) to form straight lines. If one or two adjacent marbles belonging
        to the same player are found, those spaces are also yielded as potential lines/moves.

        Yields:
            Either one or two `enums.Space`s according to the first parameter of `game.Game.move`.
        """
        lines = []
        for row_index, row in enumerate(self._board):
            if row_index == 0 or row_index == len(self._board) - 1:
                continue
            for col_index, space in enumerate(row):
                temp_lines = []
                if space is not self._current_move_color:
                    continue
                if space == self._current_move_color:
                    # getting the single marble lines
                    lines.append(
                        ((row_index, col_index), (row_index, col_index)))
                    temp_lines.append(
                        ((row_index, col_index), (row_index, col_index)))
                    # getting the group lines
                for direction in [Direction.UP_LEFT, Direction.UP_RIGHT, Direction.RIGHT]:
                    neighbor1 = self.get_neighbor(
                        (row_index, col_index), direction)
                    if neighbor1 is not None and self.get_marble(neighbor1) == self._current_move_color:
                        # adding 2 marbles
                        lines.append(((row_index, col_index), neighbor1))
                        temp_lines.append(((row_index, col_index), neighbor1))
                        neighbor2 = self.get_neighbor(neighbor1, direction)
                        if neighbor2 is not None and self.get_marble(neighbor2) == self._current_move_color:
                            # adding 3 marbles
                            lines.append(
                                ((row_index, col_index), neighbor2, neighbor1))
                            temp_lines.append(
                                ((row_index, col_index), neighbor2, neighbor1))

        return lines

    def get_next_possible_moves(self):
        for line in self.generate_own_marble_lines():
            for direction in Direction:
                # create the move from the line and check if it is a valid move
                if len(line) > 2:
                    move = Move(line[0], line[1], direction,
                                self._current_move_color, line[2])
                else:
                    move = Move(line[0], line[1], direction,
                                self._current_move_color)
                if self.validate_move(move):
                    yield move

    def generate_possible_moves(self):
        """
        Generates all possible moves for the current player from the current game state.

        This method iterates through each space on the board and, for spaces occupied by the current player's marbles,
        calculates potential moves based on predefined row and column modifiers.
        It considers both single and group moves,
        validating each move's bounds and legality within the game rules.

        Returns:
            list: A list of Move objects representing all legal moves the current player can make.
        """
        # Initialize an empty list to hold all valid moves
        moves = []
        for line in self.generate_own_marble_lines():
            for direction in Direction:
                # create the move from the line and check if it is a valid move
                if len(line) > 2:
                    move = Move(line[0], line[1], direction,
                                self._current_move_color, line[2])
                else:
                    move = Move(line[0], line[1], direction,
                                self._current_move_color)
                if self.validate_move(move):
                    moves.append(move)

        # Return the list of all valid moves
        moves.sort(key=lambda x: (x.get_move_type().value, -x.get_num_balls_moved()))
        return moves

    def convert_moves_to_board_states(self):
        """
        Converts all possible moves into corresponding board states.

        This method takes each possible move generated by `__generate_possible_moves` and applies it to the current
        game state to produce a new board representing the board after the move. This is useful for
        generating the state space for the game state.

        Returns:
            list: A list of GameState objects representing the board state after each possible move.
        """
        board_states = []

        for move in self.generate_possible_moves():
            new_board_state = self.generate_new_board_state(move)
            board_states.append(new_board_state)

        return board_states

    def convert_moves_to_game_states(self):
        """
        Converts all possible moves into corresponding game states.

        This method takes each possible move generated by `__generate_possible_moves` and applies it to the current
        game state to produce a new GameState object representing the board after the move. This is useful for
        evaluating the potential outcomes of moves.

        Returns:
            list: A list of GameState objects representing the board state after each possible move.
        """
        game_states = []

        next_marble = self._current_move_color
        if next_marble is Marble.BLACK:
            next_marble = Marble.WHITE
        elif next_marble is Marble.WHITE:
            next_marble = Marble.BLACK
        else:
            raise InvalidMarbleValue("No Marble Value provided in Set Move.")

        for move in self.generate_possible_moves():
            new_board_state = self.generate_new_board_state(move)
            new_game_state = GameState(new_board_state, move, next_marble, self)
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
        remain_ball_i_x = copy.deepcopy(first_ball_i_x)
        remain_ball_i_y = copy.deepcopy(first_ball_i_y)

        if abs(first_ball_i_x - last_ball_i_x) > 1:
            remain_ball_i_x = (first_ball_i_x + last_ball_i_x) // 2

        if abs(first_ball_i_y - last_ball_i_y) > 1:
            remain_ball_i_y = (first_ball_i_y + last_ball_i_y) // 2

        remain_ball_f_x = (first_ball_f_x + last_ball_f_x) // 2
        remain_ball_f_y = (first_ball_f_y + last_ball_f_y) // 2

        kwargs = {
            "remain_ball_i_x": remain_ball_i_x,
            "remain_ball_i_y": remain_ball_i_y,
            "first_ball_i_x": first_ball_i_x,
            "first_ball_i_y": first_ball_i_y,
            "last_ball_i_x": last_ball_i_x,
            "last_ball_i_y": last_ball_i_y,
            "remain_ball_f_x": remain_ball_f_x,
            "remain_ball_f_y": remain_ball_f_y,
            "first_ball_f_x": first_ball_f_x,
            "first_ball_f_y": first_ball_f_y,
            "last_ball_f_x": last_ball_f_x,
            "last_ball_f_y": last_ball_f_y,
            "move": move,
            "new_board": new_board
        }

        # Move Subsequent Pieces in Same Direction
        if move.get_move_type() == MoveType.INLINE:
            new_board = self.__move_subsequent_pieces(**kwargs)

        # Move the Pushers Pieces
        kwargs["new_board"] = new_board
        new_board = self.__move_pushers_pieces(**kwargs)

        return new_board

    def generate_new_game_state(self, move):
        if self._current_move_color is Marble.BLACK:
            next_marble = Marble.WHITE
        elif self._current_move_color is Marble.WHITE:
            next_marble = Marble.BLACK
        else:
            raise InvalidMarbleValue("No Marble Value provided in Set Move.")
        return GameState(self.generate_new_board_state(move), move, next_marble, self)

    def __move_subsequent_pieces(self, **kwargs):
        """
        Moves the subsequent pieces if in the way of the pushers balls (Sumito).
        :param kwargs: first and last balls
        :return:
        """
        first_ball_i_x = kwargs['first_ball_i_x']
        first_ball_i_y = kwargs['first_ball_i_y']
        last_ball_i_x = kwargs['last_ball_i_x']
        last_ball_i_y = kwargs['last_ball_i_y']

        first_ball_f_x = kwargs['first_ball_f_x']
        first_ball_f_y = kwargs['first_ball_f_y']
        new_board = kwargs['new_board']

        # Declare Multipliers to Search for Subsequent Balls
        move_x = 1 if first_ball_f_x > first_ball_i_x else (
            -1 if first_ball_f_x < first_ball_i_x else 0)
        move_y = 1 if first_ball_f_y > first_ball_i_y else (
            -1 if first_ball_f_y < first_ball_i_y else 0)

        # Declare Variables for Initial and Final Ball Positions
        sub_ball_i_x = copy.deepcopy(
            last_ball_i_x) if move_x < 0 else copy.deepcopy(first_ball_i_x)
        sub_ball_i_y = copy.deepcopy(
            last_ball_i_y) if move_y > 0 else copy.deepcopy(first_ball_i_y)
        sub_ball_f_x = copy.deepcopy(sub_ball_i_x) + move_x
        sub_ball_f_y = copy.deepcopy(sub_ball_i_y) + move_y

        # Save Original Ball Positions to keep track when Tracing Backwards
        org_ball_x = copy.deepcopy(sub_ball_i_x)
        org_ball_y = copy.deepcopy(sub_ball_i_y)

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
        while ((abs(sub_ball_i_x - org_ball_x) > 0 and move_x != 0
                or sub_ball_i_x == org_ball_x and move_x == 0)
               and
               (abs(sub_ball_i_y - org_ball_y) > 0 and move_y != 0
                or sub_ball_i_y == org_ball_y and move_y == 0)
               and not safety_lock):
            marble_color = copy.deepcopy(new_board[sub_ball_i_x][sub_ball_i_y])
            new_board[sub_ball_i_x][sub_ball_i_y] = Marble.NONE

            # If the Marble is Off the Board, Delete it. Otherwise, Move Marble to Space
            if self._board[sub_ball_f_x][sub_ball_f_y] is not None:
                new_board[sub_ball_f_x][sub_ball_f_y] = marble_color

            sub_ball_i_x -= move_x
            sub_ball_f_x -= move_x
            sub_ball_i_y -= move_y
            sub_ball_f_y -= move_y

        return new_board

    @staticmethod
    def __move_pushers_pieces(**kwargs):
        """
        Move the Pushers pieces by removing them from the original positions
        and reassigning them to the new positions.
        :param kwargs: ball positions
        :precondition: the final ball positions are empty
        :return:
        """
        remain_ball_i_x = kwargs['remain_ball_i_x']
        remain_ball_i_y = kwargs['remain_ball_i_y']
        first_ball_i_x = kwargs['first_ball_i_x']
        first_ball_i_y = kwargs['first_ball_i_y']
        last_ball_i_x = kwargs['last_ball_i_x']
        last_ball_i_y = kwargs['last_ball_i_y']

        remain_ball_f_x = kwargs['remain_ball_f_x']
        remain_ball_f_y = kwargs['remain_ball_f_y']
        first_ball_f_x = kwargs['first_ball_f_x']
        first_ball_f_y = kwargs['first_ball_f_y']
        last_ball_f_x = kwargs['last_ball_f_x']
        last_ball_f_y = kwargs['last_ball_f_y']

        move = kwargs['move']
        new_board = kwargs['new_board']

        # Remove the all the Mover's marbles in the move
        if move.get_num_balls_moved() > 2:
            new_board[remain_ball_i_x][remain_ball_i_y] = Marble.NONE
        new_board[first_ball_i_x][first_ball_i_y] = Marble.NONE
        new_board[last_ball_i_x][last_ball_i_y] = Marble.NONE

        # Place the Mover's marbles back on the board
        if move.get_num_balls_moved() > 2:
            new_board[remain_ball_f_x][remain_ball_f_y] = move.get_marble()
        new_board[first_ball_f_x][first_ball_f_y] = move.get_marble()
        new_board[last_ball_f_x][last_ball_f_y] = move.get_marble()

        return new_board

    def is_valid_single_move(self, move: Move):
        # check if the marbles are all the players color
        if (self.get_marble(move.get_pos_i()[0]) != self._current_move_color
                or self.get_marble(move.get_pos_i()[1]) != self._current_move_color):
            return False
        # if 3 long check the middle one
        if move.get_num_balls_moved() == 3 and self.get_marble(move.get_pos_i()[2]) != self._current_move_color:
            return False
        # check if the final position is on the board
        if not self._check_pos_inbounds(move.get_pos_f()[0]):
            return False
        # check if the final positions are empty
        if self.get_marble(move.get_pos_f()[0]) != Marble.NONE:
            return False
        return True

    def is_valid_sidestep_move(self, move: Move):
        # check if the move is a side step
        if move.get_move_type() != MoveType.SIDE_STEP:
            return False
        # check if the marbles are on the board
        if (move.get_pos_i()[0][0] < 1 or move.get_pos_i()[0][1] < 1
                or move.get_pos_i()[1][0] < 1 or move.get_pos_i()[1][1] < 1):
            return False
        if (move.get_pos_i()[0][0] > len(self._board) - 1
                or move.get_pos_i()[0][1] > len(self._board[0]) - 1
                or move.get_pos_i()[1][0] > len(self._board) - 1 or
                move.get_pos_i()[1][1] > len(self._board[0]) - 1):
            return False
        # check that the line is 2 or 3 marbles long
        if move.get_pos_i()[0] == move.get_pos_i()[1]:
            return False
        # check if all the final balls are on the board
        # # check that the line is straight
        # if move.get_pos_i()[0][0] == move.get_pos_i()[1][0] and move.get_pos_i()[0][1] == move.get_pos_i()[1][1]:
        #     return False

        # check that all the marbles are the player to moves color
        if (self.get_marble(move.get_pos_i()[0]) != self._current_move_color
                or self.get_marble(move.get_pos_i()[1]) != self._current_move_color):
            return False

        # check the middle one
        if move.get_num_balls_moved() == 3 and self.get_marble(move.get_pos_i()[2]) != self._current_move_color:
            return False

        # check that the final position is empty including the middle one
        for pos in move.get_pos_f():
            # Don't worry about checking the middle one if a middle ball doesn't exist (2 ball move).
            if pos[0] is None and pos[1] is None:
                continue

            # Check if Space is occupied by a ball
            if self._board[pos[0]][pos[1]] is Marble.BLACK or self._board[pos[0]][pos[1]] is Marble.WHITE:
                return False

        # check that the final positions are all on the board
        final_pos = move.get_pos_f()

        # figure out if the move is a 2 or 3 marble move
        # final ball (0,0) means that the move is a 2 marble move
        if move.get_num_balls_moved() < 3:
            # check if the final position is on the board
            if not self._check_pos_inbounds(final_pos[0]) or not self._check_pos_inbounds(final_pos[1]):
                return False
        else:
            if (not self._check_pos_inbounds(final_pos[0]) or not self._check_pos_inbounds(final_pos[1])
                    or not self._check_pos_inbounds(final_pos[2])):
                return False

        return True

    def _inline_marbles_nums(self, line: List[tuple]):
        """
        Returns the number of marbles in a line
        :param line: The line to check
        :return: The number of marbles in the line
        """
        own_marbles_num = 0
        while own_marbles_num < len(line) and self.get_marble(line[own_marbles_num]) == self._current_move_color:
            own_marbles_num += 1
        opp_marbles_num = 0
        opp_move_color = Marble.BLACK if self._current_move_color == Marble.WHITE else Marble.WHITE
        while (own_marbles_num + opp_marbles_num < len(line)
               and self.get_marble(line[own_marbles_num + opp_marbles_num]) == opp_move_color):
            opp_marbles_num += 1
        return own_marbles_num, opp_marbles_num

    def is_valid_inline_move(self, move: Move):
        # find the caboose
        neighbor_first = self.get_neighbor(
            move.get_pos_i()[0], move.get_direction())
        neighbor_last = self.get_neighbor(
            move.get_pos_i()[1], move.get_direction())
        if self.get_marble(neighbor_first) == self._current_move_color:
            caboose = move.get_pos_i()[0]
            front = move.get_pos_i()[1]
        elif self.get_marble(neighbor_last) == self._current_move_color:
            caboose = move.get_pos_i()[1]
            front = move.get_pos_i()[0]
        else:
            return False
        # check to see if the fronts neighbor is own color
        if self.get_marble(self.get_neighbor(front, move.get_direction())) == self._current_move_color:
            return False

        line = self.line_to_edge(caboose, move.get_direction())

        # Determine the number of own and opponent marbles in the line.
        own_marbles_num, opp_marbles_num = self._inline_marbles_nums(line)

        # check if there are marbles surrounding the opposite color marble
        checking_own = True
        opp_color = Marble.BLACK if self._current_move_color == Marble.WHITE else Marble.WHITE
        for pos in line:
            if self.get_marble(pos) == opp_color:
                checking_own = False
            if not checking_own and self.get_marble(pos) == self._current_move_color:
                return False
            if self.get_marble(pos) == Marble.NONE:
                break
        # check if the caboose is the current player
        if self.get_marble(caboose) != self._current_move_color:
            return False

        # check if the line has more than 3 of current player's marbles
        if own_marbles_num > 3:
            return False

        # check that own players final marbles stay on the board
        if not self._check_pos_inbounds(move.get_pos_f()[0]) or not self._check_pos_inbounds(move.get_pos_f()[1]):
            return False

        # Check if there are opponent's marbles to push (sumito condition).
        if opp_marbles_num > 0:
            # Ensure the line of opponent's marbles is shorter than the player's line, else raise an exception.
            if opp_marbles_num >= own_marbles_num:
                return False

        return True

    def validate_move(self, move: Move):
        """
        Validates a move based on the game's rules.

        Parameters:
        - move: The Move object to be validated.

        Returns:
        bool: True if the move is valid, False otherwise.
        """
        if move.get_move_type() == MoveType.SIDE_STEP:
            return self.is_valid_sidestep_move(move)
        elif move.get_move_type() == MoveType.INLINE:
            return self.is_valid_inline_move(move)
        else:
            return self.is_valid_single_move(move)

    def __check_single_move(self, **kwargs):
        # Check if the next space is an empty space
        if self._board[kwargs["ball_f_x"]][kwargs["ball_f_y"]] == Marble.NONE:
            return True
        return False

    def __check_sidestep_move(self, **kwargs):
        first_ball_f_x, first_ball_f_y, \
            remain_ball_f_x, remain_ball_f_y, \
            last_ball_f_x, last_ball_f_y, \
            num_balls_moved = map(int, kwargs.values())

        first_ball_empty = self._board[first_ball_f_x][first_ball_f_y] == Marble.NONE

        if num_balls_moved > 2:
            remain_ball_empty = self._board[remain_ball_f_x][remain_ball_f_y] == Marble.NONE
        else:
            remain_ball_empty = True

        last_ball_empty = self._board[last_ball_f_x][last_ball_f_y] == Marble.NONE

        # Check if the next space is an empty space
        if first_ball_empty and remain_ball_empty and last_ball_empty:
            return True

        return False

    def __check_inline_move(self, **kwargs):
        first_ball_i_x, first_ball_i_y, \
            last_ball_i_x, last_ball_i_y, \
            first_ball_f_x, first_ball_f_y, \
            last_ball_f_x, last_ball_f_y, \
            num_balls_moved = map(int, kwargs.values())

        # Declare Multipliers to Search for Subsequent Balls
        move_x = 1 if first_ball_f_x > first_ball_i_x else (
            -1 if first_ball_f_x < first_ball_i_x else 0)
        move_y = 1 if first_ball_f_y > first_ball_i_y else (
            -1 if first_ball_f_y < first_ball_i_y else 0)

        sub_ball_f_x = (copy.deepcopy(last_ball_f_x) if move_x <
                        0 else copy.deepcopy(first_ball_f_x))
        sub_ball_f_y = (copy.deepcopy(last_ball_f_y) if move_y >
                        0 else copy.deepcopy(first_ball_f_y))

        # Check if it is possible to push a piece
        # (Pusher outnumbers the Opponent's pieces)
        for i in range(0, num_balls_moved):
            # Check if Pushing Piece is edge of board and is on first cycle
            # (Break from Loop if True because it is your piece that is going out of bounds)
            if self._board[sub_ball_f_x][sub_ball_f_y] is None and i == 0:
                break

            # Check if Pushing Piece is edge of board
            # (return True because it is enemy piece that is going out of bounds)
            if self._board[sub_ball_f_x][sub_ball_f_y] is None:
                return True

            # Check if Edge Piece is overriding own piece (Break from Loop if True)
            if self._board[sub_ball_f_x][sub_ball_f_y] == self._current_move_color:
                break

            # Check if Space is Empty Space on the board (Return True)
            if self._board[sub_ball_f_x][sub_ball_f_y] == Marble.NONE:
                return True

            # Increment to next Cycle
            sub_ball_f_x += move_x
            sub_ball_f_y += move_y

        return False

    def _check_pos_inbounds(self, pos):
        """
        Checks if a marble is within the bounds of the board.

        Parameters:
        - pos: A tuple representing the position (row, column) of the marble.

        Returns:
        bool: True if the position is within the board's bounds; False otherwise.
        """
        if self._board[pos[0]][pos[1]] is None:
            return False
        return True

    def __check_inbounds(self, first_ball_i, last_ball_i, row):
        """
        Checks if the positions for a potential move are within the bounds of the board.

        Parameters:
        - first_ball_i: A tuple representing the initial position (row, column) of the first ball in the move.
        - last_ball_i: A tuple representing the initial position (row, column) of the last ball in the move.
        - row: The row data from the board, used to determine the bounds.

        Returns:
        bool: True if both the initial and final positions are within the board's bounds; False otherwise.
        """
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
