
from abc import ABC, abstractmethod

from app.api.enums import Marble


class Player(ABC):
    """
    An abstract base class representing a player in the game. This class defines a common interface and basic attributes for all types of players.
    """

    INIT_NUM_BALLS = 14

    def __init__(self, time_limit: int, move_limit: int,  color: Marble, num_balls: int = 14):
        """
        Initializes a Player with time and move limits, a color, and the initial number of balls.

        Parameters:
        - time_limit: The maximum amount of time (in seconds) the player is allowed to take for their moves.
        - move_limit: The maximum number of moves the player is allowed to make.
        - color: The color of the player's marbles, defined in the Marble enum.
        - numBalls: The initial number of balls (marbles) the player has at the start of the game.
        """
        self._time_limit = time_limit
        self._move_limit = move_limit
        self._current_move = 0
        self._num_balls = num_balls
        self._color = color

    @property
    def time_limit(self) -> int:
        return self._time_limit

    def move_limit(self) -> int:
        return self._move_limit

    @property
    def current_move(self) -> int:
        return self._current_move

    @current_move.setter
    def current_move(self, value: int) -> None:
        self._current_move = value

    @property
    def num_balls(self) -> int:
        return self._num_balls

    @num_balls.setter
    def num_balls(self, value: int) -> None:
        self._num_balls = value

    @property
    def color(self) -> Marble:
        return self._color

    @abstractmethod
    def make_move(self, game_manager, player, move, timestamp) -> None:
        pass

    def get_balls_remaining(self):
        return self.INIT_NUM_BALLS - self.num_balls
