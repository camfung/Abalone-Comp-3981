
from enum import Enum, auto


class Formation(Enum):
    """
    Enumeration of different starting formations
    which will be selected in the start of the game.
    """
    DEFAULT = auto()
    BELGIAN_DAISY = auto()
    GERMAN_DAISY = auto()


class Marble(Enum):
    """
    Marble Enumeration Values for GameState values in array.
    """
    WHITE = -1
    BLACK = 1
    NONE = 0


class Direction(Enum):
    """
    Direction Enumeration for Move Directions
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
