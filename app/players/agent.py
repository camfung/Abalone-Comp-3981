
import datetime
import random
import time

from app.communication.game_manager import GameManager
from app.api.enums import Marble
from app.gameplay.move import Move
from app.players.player import Player


class AbaloneAgent(Player):

    """
    A concrete implementation of the Player class representing an AI agent player.
    """

    def generate_move(self, game_manager: GameManager):
        """
        Generates a move for the AI agent based on the current game state.

        Parameters:
        - game_manager: The GameManager instance managing the game state.

        Returns:
        A tuple containing the chosen Move object and the time taken to generate the move.
        """
        initial_time = datetime.datetime.now()
        # sample for making a random move
        move = random.choice(game_manager.get_possible_moves())
        time.sleep(random.uniform(1, 3))
        final_time = datetime.datetime.now()
        time_delta = final_time - initial_time
        return move, time_delta.total_seconds()

    def make_move(self, game_manager: GameManager, player: Marble, move: Move, time_stamp: float) -> None:
        """
        Commits a move made by the AI agent to the game manager, simulating a delay before making the move.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        - time_stamp: The timestamp when the move was generated.
        """
        game_manager.commit_move(player, move, time_stamp)
