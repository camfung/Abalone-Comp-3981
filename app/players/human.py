

from app.api.enums import Marble
from app.gameplay.move import Move
from app.players.player import Player


class HumanPlayer(Player):

    """
    A concrete implementation of the Player class representing a human player.
    """

    def make_move(self, game_manager, player: Marble, move: Move, timestamp=1) -> None:
        """
        Commits a move made by the human player to the game manager.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        """
        self._current_move += 1
        print(f"\n{self._current_move}")
        game_manager.commit_move(move=move, player=player, timestamp=timestamp)
