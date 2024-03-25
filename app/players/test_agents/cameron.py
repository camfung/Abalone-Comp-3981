import datetime
import random
import sys
import time
from app.api.enums import Marble
from app.api.exceptions import InvalidMarbleValue
from app.communication.game_manager import GameManager
from app.gameplay.move import Move
from app.players.agent import AbaloneAgent



class AgentCameron(AbaloneAgent):
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
        self.time.sleep(random.uniform(1, 3))
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

    def calc_move(self, game_manager: GameManager):
        if self._color == Marble.WHITE:
            v = self.min_move(
                game_manager.get_current_game_state(), sys.maxsize * -1, sys.maxsize)
        elif self._color == Marble.BLACK:
            v = self.max_move(
                game_manager.get_current_game_state(), sys.maxsize * -1, sys.maxsize)
        else:
            raise InvalidMarbleValue(
                "Calculate Move can only be White or Black.")

        for state in game_manager.get_possible_game_states():
            if self.evaluation(state) == v:
                return state
        return None

    def calculate_group_strength(self, game_manager):
        return 0

    def calculate_board_control(self, game_manager):
        

    def calculate_marble_safety(self, game_manager):
        return 0

    def calculate_marble_cohesion(self, game_manager):
        return 0

    def calculate_opponent_disruption(self, game_manager):
        return 0

    def evaluation(self, state):
        group_strength = self.calculate_group_strength(state)
        board_control = self.calculate_board_control(state)
        marble_safety = self.calculate_marble_safety(state)
        marble_cohesion = self.calculate_marble_cohesion(state)
        opponent_disruption = self.calculate_opponent_disruption(state)

        # Assign weights based on your strategy's priorities
        weights = {'group_strength': 1.0, 'board_control': 0.8,
                   'marble_safety': 1.2, 'marble_cohesion': 0.5,
                   'opponent_disruption': 1.5}

        score = (group_strength * weights['group_strength'] +
                 board_control * weights['board_control'] +
                 marble_safety * weights['marble_safety'] +
                 marble_cohesion * weights['marble_cohesion'] +
                 opponent_disruption * weights['opponent_disruption'])

        return score
