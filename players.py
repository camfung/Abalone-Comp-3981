from abc import ABC, abstractmethod
from typing import Any


class Player(ABC):
    def __init__(self, time_limit: Any, move_limit: int, numBalls: int, color: Any):
        self._time_limit = time_limit
        self._move_limit = move_limit
        self._current_move = 0
        self._numBalls = numBalls
        self._color = color

    @property
    def time_limit(self) -> Any:
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
    def color(self) -> Any:
        return self._color

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def get_game_state(self, gameManager: Any) -> None:
        pass

    @abstractmethod
    def make_move(self, gameManager: Any, player: 'Player', move: Any) -> None:
        pass

    @abstractmethod
    def undo_last_move(self, gameManager: Any, player: 'Player', move: Any) -> None:
        pass

    @abstractmethod
    def select_player_color(self) -> None:
        pass

    @abstractmethod
    def set_move_limit(self) -> None:
        pass

    @abstractmethod
    def set_time_limit(self) -> None:
        pass
