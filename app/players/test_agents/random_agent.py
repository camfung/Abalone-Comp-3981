import datetime
import random

from app.communication.game_manager import GameManager
from app.gameplay.timer import Timer
from app.players.agent import AbaloneAgent


class RandomAgent(AbaloneAgent):
    def generate_move(self, game_manager: GameManager, timer: Timer):
        """
        Generates a move for the AI agent based on the current game state.

        Parameters:
        - game_manager: The GameManager instance managing the game state.

        Returns:
        A tuple containing the chosen Move object and the time taken to generate the move.
        """
        initial_time = datetime.datetime.now()

        # Decide if the move is going to be random or calculated.
        move = random.choice(game_manager.get_possible_moves())

        final_time = datetime.datetime.now()
        time_delta = final_time - initial_time
        return move, time_delta.total_seconds()
