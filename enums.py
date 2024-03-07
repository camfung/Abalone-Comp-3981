
from enum import *


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
    UP_LEFT = auto()
    UP_RIGHT = auto()
    RIGHT = auto()
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()
    LEFT = auto()


class MarbleSelection(Enum):
    """
    Marble Selection Enumeration for Marble Selections in Generate Possible Moves.
    """
    HORIZONTAL = auto()
    BACKWARD_SLASH = auto()
    FORWARD_SLASH = auto()
    SINGLE = auto()


class MoveType(Enum):
    """
    Move Type Enumeration for type of move made by Player
    """
    SINGLE = auto()
    INLINE = auto()
    SIDE_STEP = auto()


class UIState(Enum):
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    PLAY_MENU = auto()
    GAME_PLAY = auto()


class GameType(Enum):
    PLAYER_VS_PLAYER = auto()
    PLAYER_VS_CPU = auto()
    CPU_VS_CPU = auto()


class PlayerInputEvents(Enum):
    AWAITING_FIRST_MARBLE = auto()
    AWAITING_SECOND_MARBLE = auto()
    AWAITING_DIRECTION = auto()
