
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
    INLINE = auto()
    SIDE_STEP = auto()
    SINGLE = auto()


class UIState(Enum):
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    PLAY_MENU = auto()
    GAME_PLAY = auto()


class GameType(Enum):
    """
    Enum representing the types of games in the Abalone-Comp-3981 project.

    Attributes:
        PLAYER_VS_PLAYER: Represents a game between two human players.
        PLAYER_VS_AGENT: Represents a game between a human player and an agent.
        AGENT_VS_AGENT: Represents a game between two agents.
    """
    PLAYER_VS_PLAYER = auto()
    PLAYER_VS_AGENT = auto()
    AGENT_VS_AGENT = auto()


class PlayerInputEvents(Enum):
    """
    Enum representing the different input events for a player.

    Attributes:
        AWAITING_FIRST_MARBLE: Represents the state when the player is awaiting the selection of the first marble.
        AWAITING_SECOND_MARBLE: Represents the state when the player is awaiting the selection of the second marble.
        AWAITING_DIRECTION: Represents the state when the player is awaiting the selection of the movement direction.
    """
    AWAITING_FIRST_MARBLE = auto()
    AWAITING_SECOND_MARBLE = auto()
    AWAITING_DIRECTION = auto()
