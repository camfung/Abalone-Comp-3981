from abc import ABC, abstractmethod
import random
import time
from typing import Any

from communication import GameManager
from enums import Marble
from gameplay import Move


class Player(ABC):
    INIT_NUM_BALLS = 14

    def __init__(self, time_limit: int, move_limit: int,  color: Marble, numBalls: int = 14):
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

    @abstractmethod
    def undo_last_move(self, game_manager, player, move) -> None:
        pass

    def get_balls_remaining(self):
        return self.INIT_NUM_BALLS - self.numBalls


class HumanPlayer(Player):

    def make_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        gameManager.commit_move(move)

    def undo_last_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        print("Undoing last move.")


class AbaloneAgent(Player):

    def generate_move(self, gameManager: GameManager):
        # sample for making a random move
        move = random.choice(
            gameManager.get_possible_moves())
        return move

    def make_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        time.sleep(1)
        gameManager.commit_move(player, move, None)

    def undo_last_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        print("Agent undoing last move.")
