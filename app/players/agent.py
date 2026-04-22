
import abc
import datetime
import math
import random
import multiprocessing
import time

from app.communication.game_manager import GameManager
from app.api.enums import Marble
from app.gameplay.game_state import GameState
from app.gameplay.move import Move
from app.gameplay.timer import Timer
from app.players.player import Player


class AbaloneAgent(Player):
    """
    A concrete implementation of the Player class representing an AI agent player.
    """

    def __init__(self, time_limit: int, move_limit: int, color: Marble):
        super().__init__(time_limit, move_limit, color)

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
        if self._current_move <= 0 and self.color == Marble.BLACK:
            move = random.choice(game_manager.get_possible_moves())
        else:
            move = self.calc_move(game_manager)

        final_time = datetime.datetime.now()
        time_delta = final_time - initial_time
        return move, time_delta.total_seconds()

    def make_move(self, game_manager: GameManager, player: Marble, move: Move, timestamp: float) -> None:
        """
        Commits a move made by the AI agent to the game manager, simulating a delay before making the move.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        - time_stamp: The timestamp when the move was generated.
        """
        # AI will not generate move if game is over
        if game_manager.app.players[0].num_balls < 9 or game_manager.app.players[1].num_balls < 9:
            return

        self._current_move += 1
        game_manager.commit_move(player, move, timestamp)

    def calc_move(self, game_manager: GameManager) -> Move:
        start_time = time.time()
        best_move = None
        depth = 1
        max_depth = self._move_limit - self._current_move

        num_processes = multiprocessing.cpu_count()
        current_game_state = game_manager.get_current_game_state()

        while depth <= max_depth:
            # Check if time limit has been reached
            if self.running_out_of_time(start_time):
                break

            pool = multiprocessing.Pool(num_processes)
            batch_results = pool.starmap(self.evaluate_subtree, [(game_state, distance, start_time)
                                                                 for distance in range(1, depth + 1, 1)
                                                                 for game_state in current_game_state.convert_moves_to_game_states()])
            pool.close()

            # Check if time limit has been reached
            if self.running_out_of_time(start_time):
                pool.terminate()
                break
            else:
                pool.join()

            valid_results = [result for result in batch_results if result is not None]

            v, best_move = self.combine_results(valid_results)

            # Return move immediately if it wins agent the game
            if v == math.inf:
                break

            print(f"Depth {depth} Finished")
            depth += 1

        return best_move if best_move is not None else None

    def evaluate_subtree(self, game_state: GameState, depth: int, start_time):
        transposition_table = {}
        killer_moves = {}

        v, v_state = self.min_move(game_state, -math.inf, math.inf, depth, transposition_table, start_time, killer_moves)

        return (v, game_state.get_move()) if not self.running_out_of_time(start_time) else None

    @staticmethod
    def combine_results(depth_results):
        best_v, best_v_move = -math.inf, None
        for result in depth_results:
            v, v_move = result
            if v > best_v:
                best_v, best_v_move = v, v_move
            if best_v == math.inf:
                break

        return best_v, best_v_move

    @staticmethod
    def terminal_test(state: GameState) -> bool:
        """
        Checks if the endgame condition is met.
        :param state: GameState
        :return: boolean indicating end game condition met
        """
        if state.white_balls <= 8:
            return True
        if state.black_balls <= 8:
            return True

        return False

    @abc.abstractmethod
    def evaluation(self, state):
        """
        Evaluate the current state based on heuristics.

        Heuristics will be implemented in Part 3.
        :param state: GameState
        :return: Evaluation Value as an integer.
        """
        pass

    def running_out_of_time(self, start_time):
        if time.time() - start_time > self.time_limit - 1:
            return True
        return False

    def max_move(self, state: GameState, alpha, beta, distance: int, transposition_table, start_time, killer_moves):
        """
        Calculate Best Black Move.
        :param start_time: Time
        :param transposition_table:
        :param killer_moves: dict mapping depth -> list of moves that caused beta cutoffs
        :param state: GameState
        :param alpha: White's Best Value (Int)
        :param beta: Black's Best Value (Int)
        :param distance: Iterative Deepening Distance (Int)
        :return: Tuple of Best Value and Best State for Black
        """
        if self.terminal_test(state) or distance <= 0 or self.running_out_of_time(start_time):
            return self.evaluation(state), state

        v, v_state = self.board_value_in_transposition_table(state.get_board(), transposition_table)
        if (v, v_state) != (None, None):
            return v, state

        best_value = -math.inf
        best_state = None
        new_distance = distance - 1

        killer_keys = {self._move_key(k) for k in killer_moves.get(distance, [])}
        for move, child_state in self._get_ordered_children(state, killer_keys, maximize=True):
            v, v_state = self.min_move(child_state, alpha, beta, new_distance, transposition_table, start_time, killer_moves)

            if v > best_value:
                best_value = v
                best_state = child_state

            if best_value >= beta or self.running_out_of_time(start_time):
                self._store_killer(killer_moves, distance, move)
                break

            alpha = max(alpha, best_value)

        self.add_board_hash_to_transposition_table(best_state, best_value, transposition_table)
        return best_value, best_state

    def min_move(self, state: GameState, alpha, beta, distance: int, transposition_table, start_time, killer_moves):
        """
        Calculate Best White Move.
        :param start_time: Time
        :param transposition_table:
        :param killer_moves: dict mapping depth -> list of moves that caused alpha cutoffs
        :param state: GameState
        :param alpha: White's Best Value (Int)
        :param beta: Black's Best Value (Int)
        :param distance: Iterative Deepening Distance (Int)
        :return: Tuple of Best Value and Best State for White
        """
        if self.terminal_test(state) or distance <= 0 or self.running_out_of_time(start_time):
            return self.evaluation(state), state

        v, v_state = self.board_value_in_transposition_table(state.get_board(), transposition_table)
        if (v, v_state) != (None, None):
            return v, state

        best_value = math.inf
        best_state = None
        new_distance = distance - 1

        killer_keys = {self._move_key(k) for k in killer_moves.get(distance, [])}
        for move, child_state in self._get_ordered_children(state, killer_keys, maximize=False):
            v, v_state = self.max_move(child_state, alpha, beta, new_distance, transposition_table, start_time, killer_moves)

            if v < best_value:
                best_value = v
                best_state = child_state

            if best_value <= alpha or self.running_out_of_time(start_time):
                self._store_killer(killer_moves, distance, move)
                break

            beta = min(beta, best_value)

        self.add_board_hash_to_transposition_table(best_state, best_value, transposition_table)
        return best_value, best_state

    def _get_ordered_children(self, state: GameState, killer_keys: set, maximize: bool):
        """
        Generate all child states, score each with the evaluation heuristic, and return
        (move, child_state) pairs ordered so the most-promising moves come first.
        Killer moves (those that caused cutoffs in sibling nodes) are always tried first.
        """
        killers = []
        others = []
        for move in state.generate_possible_moves():
            child = state.generate_new_game_state(move)
            score = self.evaluation(child)
            if self._move_key(move) in killer_keys:
                killers.append((score, move, child))
            else:
                others.append((score, move, child))

        others.sort(key=lambda x: x[0], reverse=maximize)
        return [(m, c) for _, m, c in killers + others]

    @staticmethod
    def _move_key(move):
        return (move.get_pos_i(), move.get_direction(), move.get_marble())

    @staticmethod
    def _store_killer(killer_moves, depth, move):
        killers = killer_moves.setdefault(depth, [])
        key = AbaloneAgent._move_key(move)
        if key not in [AbaloneAgent._move_key(k) for k in killers]:
            killers.insert(0, move)
            if len(killers) > 2:
                killers.pop()

    @staticmethod
    def add_board_hash_to_transposition_table(state, value, transposition_table):
        """
        Add State, Value Pair to Transposition Table
        :param transposition_table: dict
        :param state: GameState
        :param value: Board Value (Int)
        :return:
        """
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in state.get_board()))

        # Add Hash and Value to Transposition Table
        transposition_table[board_hash] = value, state

    @staticmethod
    def board_value_in_transposition_table(board, transposition_table):
        """
        Get Board Value and its stored GameState in Transposition Table.
        :param transposition_table:
        :param board: 2D List
        :return: Board Value (int), GameState
        """
        # Hash the Board
        board_hash = hash(tuple(tuple(row) for row in board))

        # Try to get Value of Board from Transposition Table
        try:
            value, state = transposition_table[board_hash]
            return value, state
        except KeyError:
            return None, None
