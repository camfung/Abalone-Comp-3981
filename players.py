from abc import ABC, abstractmethod
import datetime
import random
import time
from typing import Any

from communication import GameManager
from enums import Marble
from gameplay import Move


class Player(ABC):
    """
    An abstract base class representing a player in the game. This class defines a common interface and basic attributes for all types of players.
    """

    INIT_NUM_BALLS = 14

    def __init__(self, time_limit: int, move_limit: int,  color: Marble, numBalls: int = 14):
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
        self._numBalls = numBalls
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
    def numBalls(self) -> int:
        return self._numBalls

    @numBalls.setter
    def numBalls(self, value: int) -> None:
        self._numBalls = value

    @property
    def color(self) -> int:
        return self._color

    @abstractmethod
    def make_move(self, game_manager, player, move) -> None:
        pass

    def get_balls_remaining(self):
        return self.INIT_NUM_BALLS - self.numBalls


class HumanPlayer(Player):

    """
    A concrete implementation of the Player class representing a human player.
    """

    def make_move(self, gameManager: GameManager, player: Marble, move: Move) -> None:
        """
        Commits a move made by the human player to the game manager.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        """
        gameManager.commit_move(move=move, player=player, timestamp=1)


class AbaloneAgent(Player):

    """
    A concrete implementation of the Player class representing an AI agent player.
    """

    def generate_move(self, gameManager: GameManager):
        """
        Generates a move for the AI agent based on the current game state.

        Parameters:
        - game_manager: The GameManager instance managing the game state.

        Returns:
        A tuple containing the chosen Move object and the time taken to generate the move.
        """
        initial_time = datetime.datetime.now()
        # sample for making a random move
        move = random.choice(
            gameManager.get_possible_moves())
        time.sleep(random.uniform(1, 3))
        final_time = datetime.datetime.now()
        timeDelta = final_time - initial_time
        return move, timeDelta.total_seconds()

    def make_move(self, gameManager: GameManager, player: Marble, move: Move, time_stamp: float) -> None:
        """
        Commits a move made by the AI agent to the game manager, simulating a delay before making the move.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        - time_stamp: The timestamp when the move was generated.
        """
        gameManager.commit_move(player, move, time_stamp)
