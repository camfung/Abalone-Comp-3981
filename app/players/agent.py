
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
        if self._color == Marble.WHITE:
            best_value = math.inf
            for distance in range(1, 25, 1):
                self._transposition_table = {}
                v = self.min_move(game_manager.get_current_game_state(), -math.inf, math.inf, distance)
                if best_value < v:
                    best_value = v
        elif self._color == Marble.BLACK:
            best_value = -math.inf
            for distance in range(1, 25, 1):
                self._transposition_table = {}
                v = self.max_move(game_manager.get_current_game_state(), -math.inf, math.inf, distance)
                if best_value > v:
                    best_value = v
        else:
            raise InvalidMarbleValue("Calculate Move can only be White or Black.")

        for state in game_manager.get_possible_game_states():
            if self.evaluation(state) == best_value:
                return state
        return None

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

    def max_move(self, state: GameState, alpha, beta, distance):
        # Check if Position is in Transposition Table
        v = self.board_value_in_transposition_table(state.get_board())
        if v is not None:
            return v

        # if Terminal Test state return Utility
        if self.terminal_test(state) or distance <= 0:
            return self.evaluation(state)

        # Assign Lowest Value
        v = -math.inf

        # Check each possible state from current game state
        for child_states in state.convert_moves_to_game_states():
            v = max(v, self.min_move(child_states, alpha, beta, distance - 1))
            if v > beta:
                break
            alpha = max(alpha, v)
        self.add_board_hash_to_transposition_table(state.get_board(), v)
        return v

    def min_move(self, transposition_table, state: GameState, alpha, beta, distance):
        # if Terminal Test state return Utility
        if self.terminal_test(state) or distance <= 0:
            return self.evaluation(state)

        # Check if Position is in Transposition Table
        v = self.board_value_in_transposition_table(state.get_board(), transposition_table)
        if v is not None:
            return v

        # Assign Highest Value
        v = math.inf

        # Check each possible state from current game state
        for child_states in state.convert_moves_to_game_states():
            v = min(v, self.max_move(transposition_table, child_states, alpha, beta, distance - 1))
            if v < alpha:
                break
            beta = max(alpha, v)
        self.add_board_hash_to_transposition_table(state.get_board(), v)
        return v

    def add_board_hash_to_transposition_table(self, board, value):
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in board))

        # Add Hash and Value to Transposition Table
        self._transposition_table[board_hash] = value

    def board_value_in_transposition_table(self, board):
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in board))

        # Try to get Value of Board from Transposition Table
        try:
            value = self._transposition_table[board_hash]
            return value
        except KeyError:
            return None
