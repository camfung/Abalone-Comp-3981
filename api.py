
import abc


class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass


class Move:
    def __init__(self, first_ball_i, last_ball_i, first_ball_f, last_ball_f, direction, player):
        self._pos_i = (first_ball_i, last_ball_i)
        self._pos_f = (first_ball_f, last_ball_f)
        self._direction = direction
        self._player = player

    def __str__(self):
        return f"{self._pos_i} -> {self._pos_f}"
