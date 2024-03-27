import copy
import datetime
import math
import random
import time

from app.api.exceptions import InvalidMarbleValue
from app.communication.game_manager import GameManager
from app.api.enums import Marble
from app.gameplay.game_state import GameState
from app.gameplay.move import Move
from app.players.player import Player


class AbaloneAgent(Player):
    """
    A concrete implementation of the Player class representing an AI agent player.
    """
    def __init__(self, time_limit: int, move_limit: int, color: Marble):
        super().__init__(time_limit, move_limit, color)
        self._transposition_table = {}

    def generate_move(self, game_manager: GameManager):
        """
        Generates a move for the AI agent based on the current game state.

        Parameters:
        - game_manager: The GameManager instance managing the game state.

        Returns:
        A tuple containing the chosen Move object and the time taken to generate the move.
        """
        initial_time = datetime.datetime.now()

        # Decide if the move is going to be random or calculated.
        if self._current_move <= 0 and self._color == Marble.BLACK:
            move = random.choice(game_manager.get_possible_moves())
            time.sleep(random.uniform(1, 3))
        else:
            move = self.calc_move(game_manager)

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
        best_state = None
        if self._color == Marble.WHITE:
            best_value = math.inf
            for distance in range(1, 25, 1):
                self._transposition_table = {}
                v, v_state = self.white_move(game_manager.get_current_game_state(), -math.inf, math.inf, distance)
                print(v)
                if best_value > v:
                    best_value = v
                    best_state = copy.deepcopy(v_state)
        elif self._color == Marble.BLACK:
            best_value = -math.inf
            for distance in range(1, 25, 1):
                self._transposition_table = {}
                v, v_state = self.black_move(game_manager.get_current_game_state(), -math.inf, math.inf, distance)
                if best_value < v:
                    best_value = v
                    best_state = copy.deepcopy(v_state)
        else:
            raise InvalidMarbleValue("Calculate Move can only be White or Black.")

        return best_state.get_move() if best_state else None

    @staticmethod
    def terminal_test(state: GameState) -> bool:
        white_balls, black_balls = state.get_ball_count()

        if white_balls <= 8:
            return True
        if black_balls <= 8:
            return True

        return False

    @classmethod
    def evaluation(cls, state):
        """
        Evaluate the current state based on heuristics.

        Heuristics will be implemented in Part 3.
        :param state: GameState
        :return: Evaluation Value as an integer.
        """
        return 0

    def black_move(self, state: GameState, alpha, beta, distance):
        """
        Calculate Best Black Move.
        :param state: GameState
        :param alpha: White's Best Value (Int)
        :param beta: Black's Best Value (Int)
        :param distance: Iterative Deepening Distance (Int)
        :return: Tuple of Best Value and Best State for Black
        """
        # if Terminal Test state return Utility
        if self.terminal_test(state) or distance <= 0:
            return self.evaluation(state), state

        # Check if Position is in Transposition Table
        v, v_state = self.board_value_in_transposition_table(state.get_board())
        if (v, v_state) != (None, None):
            return v, v_state

        # Assign Lowest Value
        best_value = -math.inf
        best_state = None

        # Check each possible state from current game state
        for child_states in state.convert_moves_to_game_states():
            # Get White's Best State
            v, v_state = self.white_move(child_states, alpha, beta, distance - 1)

            # Re-assign Best Value if White's Best State is better than the current Best State
            if v > best_value:
                best_value = v
                best_state = v_state

            # Prune Branch if White's Best State is better than current best White State
            if best_value > beta:
                break
            alpha = max(alpha, v)

        # Add Best State to Transposition Table
        self.add_board_hash_to_transposition_table(best_state, best_value)
        return best_value, best_state

    def white_move(self, state: GameState, alpha, beta, distance):
        """
        Calculate Best White Move
        :param state: GameState
        :param alpha: White's Best Value (Int)
        :param beta: Black's Best Value (Int)
        :param distance: Iterative Deepening Distance (Int)
        :return: Tuple of Best Value and Best State for White
        """
        # if Terminal Test state return Utility
        if self.terminal_test(state) or distance <= 0:
            return self.evaluation(state), state

        # Check if Position is in Transposition Table
        v, v_state = self.board_value_in_transposition_table(state.get_board())
        if (v, v_state) != (None, None):
            return v, v_state

        # Assign Highest Value
        best_value = math.inf
        best_state = None

        # Check each possible state from current game state
        for child_states in state.convert_moves_to_game_states():
            # Get Best Black State
            v, v_state = self.black_move(child_states, alpha, beta, distance - 1)

            # Re-assign Best Value if Black's Best State is better than the current Best State
            if v < best_value:
                best_value = v
                best_state = copy.deepcopy(v_state)

            # Prune Branch if Black's Best State is better than current best Black State
            if best_value < alpha:
                break
            beta = max(alpha, v)

        # Add Best State to Transposition Table
        self.add_board_hash_to_transposition_table(best_state, best_value)
        return best_value, best_state

    def add_board_hash_to_transposition_table(self, state, value):
        """
        Add State, Value Pair to Transposition Table
        :param state: GameState
        :param value: Board Value (Int)
        :return:
        """
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in state.get_board()))

        # Add Hash and Value to Transposition Table
        self._transposition_table[board_hash] = value, state

    def board_value_in_transposition_table(self, board):
        """
        Get Board Value and its stored GameState in Transposition Table.
        :param board: 2D List
        :return: Board Value (int), GameState
        """
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in board))

        # Try to get Value of Board from Transposition Table
        try:
            value, state = self._transposition_table[board_hash]
            return value, state
        except KeyError:
            return None, None
