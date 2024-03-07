from abc import ABC, abstractmethod
from typing import Any


class GameManager:
    pass


class Move:
    pass


class Player(ABC):
    INIT_NUM_BALLS = 14

    def __init__(self, time_limit: int, move_limit: int, numBalls: int, color: int):
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
    def update(self) -> None:
        pass

    # I'm not sure if this is necessary.
    # wouldnt all the interaction with the game state be in the make move function.
    # if so then the child classes can get the state from the gamemanager since it will be in the scope of the function
    @abstractmethod
    def get_game_state(self, gameManager: GameManager) -> None:
        return gameManager.get_game_state()

    @abstractmethod
    def make_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        pass

    @abstractmethod
    def undo_last_move(self, gameManager: GameManager, player: 'Player', move: Move) -> None:
        pass

    def get_balls_remaining(self):
        return self.INIT_NUM_BALLS - self.numBalls
