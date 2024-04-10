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
        self.subtrees = None
        self.terminated = False
        self.result_ready_event = multiprocessing.Event()

    def internal_timer(self):
        time_left = self.time_limit - 1
        while time_left > 0:
            time_left -= 1
            time.sleep(1)
        print("Running out of time. Terminating all processes.")
        self.terminated = True
        self.result_ready_event.set()

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

    @staticmethod
    def split_list(lst, num_splits):
        """
        Splits a list into a given number of approximately equal-sized parts.

        Args:
        lst (list): The list to be split.
        num_splits (int): The number of parts to split the list into.

        Returns:
        list of lists: A list containing 'num_splits' sublists.
        """
        # Calculate the length of each part
        part_size = len(lst) // num_splits
        remainder = len(lst) % num_splits

        # Calculate the end indices for each part
        end_indices = [part_size * (i + 1) + min(i, remainder) for i in range(num_splits)]

        # Use list comprehension to split the list
        split_list_result = [lst[start:end_indices[i]] for i, start in enumerate([0] + end_indices[:-1])]

        return split_list_result

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
        self.terminated = False
        best_state = None
        max_range = self._move_limit - self._current_move

        num_processes = multiprocessing.cpu_count()

        self.subtrees = self.split_list(game_manager.get_possible_game_states(), num_processes)

        pool = multiprocessing.Pool(num_processes)
        timer_thread = multiprocessing.Process(target=self.internal_timer)
        timer_thread.start()

        for distance in range(0, max_range + 1, 1):
            print(f"Distance: {distance}")
            results = pool.map(self.evaluate_subtree, [(subtree, distance) for subtree in self.subtrees])

            self.result_ready_event.wait()

            print("Something happened.")

            if self.terminated:
                pool.terminate()
                pool.join()
                break

            pool.join()

            print(f"\nFinished Distance {distance}")
            print(results)

            v, best_state = self.combine_results(results)
            print(f"Current Best Move: [{v}, {str(best_state.get_move())}]")

            # Return move immediately if it wins agent the game
            if v == math.inf:
                break

        self.terminated = False

        return best_state.get_move() if best_state is not None else None

    def evaluate_subtree(self, sub_tree_list, depth: int):
        print("Started Evaluating Chunk")
        transposition_table = {}

        results = []
        for sub_tree in sub_tree_list:
            v, v_state = self.min_move(sub_tree, -math.inf, math.inf, depth, transposition_table)
            results.append((v, v_state))
            print(f"Evaluate Subtree: [{v}, {str(v_state.get_move())}]")

        print("Finished Evaluating Subtrees.")
        best_result = self.combine_results(results)
        self.result_ready_event.set()
        print("Finished Combining the Subtree result. Wrapping up now.")
        return best_result

    @staticmethod
    def combine_results(results):
        print("Combining Results...")
        best_v, best_v_state = -math.inf, None
        for result in results:
            v, v_state = result
            if v > best_v:
                best_v, best_v_state = v, v_state
            if best_v == math.inf:
                break

        print(f"Finished Combining Results: [{best_v}, {str(best_v_state.get_move())}]")
        return best_v, best_v_state

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

    def max_move(self, state: GameState, alpha, beta, distance: int, transposition_table):
        """
        Calculate Best Black Move.
        :param transposition_table:
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
        v, v_state = self.board_value_in_transposition_table(state.get_board(), transposition_table)
        if (v, v_state) != (None, None):
            return v, state

        # Assign Lowest Value
        best_value = -math.inf
        best_state = None

        # Decrement Distance if the move is your color
        if self._color == state.get_current_move_color():
            new_distance = distance - 1
        else:
            new_distance = distance

        possible_moves = state.get_next_possible_moves()

        # Check each possible state from current game state
        while True:
            try:
                child_state = state.generate_new_game_state(next(possible_moves))

                # Get White's Best State
                v, v_state = self.min_move(child_state, alpha, beta, new_distance, transposition_table)

                # Re-assign Best Value if White's Best State is better than the current Best State
                if v > best_value:
                    best_value = v
                    best_state = child_state

                # Prune Branch if White's Best State is better than current best White State
                if best_value >= beta:
                    break

                alpha = max(alpha, best_value)
            except StopIteration:
                break

        # Add Best State to Transposition Table
        self.add_board_hash_to_transposition_table(best_state, best_value, transposition_table)
        return best_value, best_state

    def min_move(self, state: GameState, alpha, beta, distance: int, transposition_table):
        """
        Calculate Best White Move
        :param transposition_table:
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
        v, v_state = self.board_value_in_transposition_table(state.get_board(), transposition_table)
        if (v, v_state) != (None, None):
            return v, state

        # Assign Highest Value
        best_value = math.inf
        best_state = None

        # Decrement Distance if the move is your color
        if self._color == state.get_current_move_color():
            new_distance = distance - 1
        else:
            new_distance = distance

        possible_moves = state.get_next_possible_moves()

        # Check each possible state from current game state
        while True:
            try:
                move = next(possible_moves)
                child_state = state.generate_new_game_state(move)

                # Get Best Black State
                v, v_state = self.max_move(child_state, alpha, beta, new_distance, transposition_table)

                # Re-assign Best Value if Black's Best State is better than the current Best State
                if v < best_value:
                    best_value = v
                    best_state = child_state

                # Prune Branch if Black's Best State is better than current best Black State
                if best_value <= alpha:
                    break
                beta = min(beta, best_value)
            except StopIteration:
                break

        # Add Best State to Transposition Table
        self.add_board_hash_to_transposition_table(best_state, best_value, transposition_table)
        return best_value, best_state

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
