
from app.communication.game_manager import GameManager
from app.enums import Marble
from app.gameplay.move import Move
from app.players.player import Player


class HumanPlayer(Player):

    """
    A concrete implementation of the Player class representing a human player.
    """

    def make_move(self, game_manager: GameManager, player: Marble, move: Move) -> None:
        """
        Commits a move made by the human player to the game manager.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        """
        game_manager.commit_move(move=move, player=player, timestamp=1)
