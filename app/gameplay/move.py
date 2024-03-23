import copy

from app.api.enums import *
from app.api.exceptions import InvalidDirection


class Move:
    """
    Represents a move in the game, including its start and end positions, direction, marble involved, and move type.
    """

    def __init__(self, first_ball_i, last_ball_i, direction, marble, middle_ball_i=(0, 0)):
        """
        Initializes a new move with specified parameters.

        Parameters:
        - first_ball_i: The initial position of the first ball in the move (row, column).
        - last_ball_i: The initial position of the last ball in the move (row, column),
        for moves involving multiple balls.
        - direction: The direction of the move, defined in the Direction enum.
        - marble: The type of marble being moved, defined in the Marble enum.
        """
        self._direction = direction
        self._marble = marble
        self._pos_i = (first_ball_i, last_ball_i, middle_ball_i)
        self._pos_f = Move.__calc_pos_f(
            first_ball_i, last_ball_i, direction, middle_ball_i)
        self._selection_type = Move.__calc_selection_type(
            first_ball_i, last_ball_i)
        self._move_type = Move.__calc_move_type(
            first_ball_i, last_ball_i, direction, self._selection_type)
        self._num_balls_moved = Move.__calc_num_balls_moved(
            first_ball_i, last_ball_i)

    @property
    def marble(self):
        return self._marble

    @staticmethod
    def __calc_pos_f(f_ball_i, l_ball_i, direction, m_ball_i=None):
        """
        Calculates the final positions of the balls after the move.

        Parameters:
        - first_ball_i: Initial position of the first ball.
        - last_ball_i: Initial position of the last ball.
        - direction: The direction of the move.

        Returns:
        Tuple containing the final positions of the first and last balls.
        """
        first_ball_i = copy.deepcopy(f_ball_i)
        last_ball_i = copy.deepcopy(l_ball_i)
        middle_ball_i = copy.deepcopy(m_ball_i)

        try:
            position = ((first_ball_i[0] + direction.value[0], first_ball_i[1] + direction.value[1]),
                        (last_ball_i[0] + direction.value[0], last_ball_i[1] + direction.value[1]),
                        (middle_ball_i[0] + direction.value[0], middle_ball_i[1] + direction.value[1])
            )
            return position
        except TypeError:
            raise InvalidDirection("Direction passed to Move is None")

    @staticmethod
    def __calc_selection_type(first_ball_i, last_ball_i):
        """
        Determines the selection type of the move based on the initial positions of the balls.

        Parameters:
        - first_ball_i: Initial position of the first ball.
        - last_ball_i: Initial position of the last ball.

        Returns:
        MarbleSelection: The selection type (horizontal, backward slash, forward slash).
        """
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
        """
        Determines the type of move based on the initial positions of the balls, their selection type, and direction.

        Parameters:
        - first_ball_i: Initial position of the first ball.
        - last_ball_i: Initial position of the last ball.
        - direction: The direction of the move.
        - selection: The selection type of the move.

        Returns:
        MoveType: The type of the move (single, inline, side step).
        """
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

    @staticmethod
    def __calc_num_balls_moved(first_ball_i, last_ball_i):
        """
        Calculates the number of balls being moved.

        :param first_ball_i: first ball position
        :param last_ball_i: last ball position
        :return: integer representing the number of balls being moved.
        """

        # Check if 3 balls are being moved
        if (abs(first_ball_i[0] - last_ball_i[0]) > 1
                or abs(first_ball_i[1] - last_ball_i[1]) > 1):
            return 3

        if first_ball_i != last_ball_i:
            return 2

        return 1

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

    def get_num_balls_moved(self):
        return self._num_balls_moved

    def __str__(self):
        char_first_i_x = chr(self._pos_i[0][0] + 74 - 2 * (self._pos_i[0][0]))
        char_first_f_x = chr(self._pos_f[0][0] + 74 - 2 * (self._pos_f[0][0]))
        char_last_i_x = chr(self._pos_i[1][0] + 74 - 2 * (self._pos_i[1][0]))
        char_last_f_x = chr(self._pos_f[1][0] + 74 - 2 * (self._pos_f[1][0]))

        if self._move_type == MoveType.SINGLE:
            return (f"{char_first_i_x}{self._pos_i[0][1]} "
                    f"-> {char_first_f_x}{self._pos_f[0][1]}")
        return (f"{char_first_i_x}{self._pos_i[0][1]}, "
                f"{char_last_i_x}{self._pos_i[1][1]} "
                f"-> {char_first_f_x}{self._pos_f[0][1]}, "
                f"{char_last_f_x}{self._pos_f[1][1]}")

    def move_notation_str(self):
        """
        String representation of the move that matches the report format
        :return: String
        """
        char_first_i_x = chr(self._pos_i[0][0] + 74 - 2 * (self._pos_i[0][0]))
        char_first_f_x = chr(self._pos_f[0][0] + 74 - 2 * (self._pos_f[0][0]))
        char_last_i_x = chr(self._pos_i[1][0] + 74 - 2 * (self._pos_i[1][0]))
        char_last_f_x = chr(self._pos_f[1][0] + 74 - 2 * (self._pos_f[1][0]))

        return (f"({char_first_i_x}{self._pos_i[0][1]}, "
                f"{char_last_i_x}{self._pos_i[1][1]}) "
                f"-> ({char_first_f_x}{self._pos_f[0][1]}, "
                f"{char_last_f_x}{self._pos_f[1][1]}) {self._move_type.name} {self._marble.name}")
