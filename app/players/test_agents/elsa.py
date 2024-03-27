from app.players.agent import AbaloneAgent

import datetime
import random
import sys
import time
from app.api.exceptions import InvalidMarbleValue
from app.communication.game_manager import GameManager
from app.api.enums import Marble, Direction
from app.gameplay.game_state import GameState
from app.gameplay.move import Move
from app.players.player import Player


class AgentElsa(AbaloneAgent):
    def generate_move(self, game_manager):
        """
        Generates a move for the AI agent based on the current game state.

        Parameters:
        - game_manager: The GameManager instance managing the game state.

        Returns:
        A tuple containing the chosen Move object and the time taken to generate the move.
        """

        initial_time = datetime.datetime.now()

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
        if self._current_move == 0 and self.color == Marble.WHITE:
            game_manager.commit_move(player, self.opening_moves(game_manager), time_stamp)
            self.calc_center_distance(game_manager.get_current_game_state()._board) #Test
            print("move made")
            return
        print("2move made")
        game_manager.commit_move(player, move, time_stamp)

    def opening_moves(self, game_manager):  # Test
        if self.color == Marble.BLACK:
            if self._current_move == 0:
                return random.choice(game_manager.get_possible_moves())
        else:
            if self._current_move == 1:
                return Move(((9, 5), (7, 5)), ((8, 5), (6, 5)), Direction.DOWN_RIGHT, marble=self.color)

        return random.choice(game_manager.get_possible_moves())

    @staticmethod
    def calc_center_distance(board):
        """
        Calculates the distance from the center of the board
        :param board:
        :return:
        """
        mid_index = (5, 5)

        white_dist = 0
        black_dist = 0
        white_count = 0
        black_count = 0

        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if col == Marble.BLACK:
                    black_dist += abs(mid_index[0] - row_index) + abs(mid_index[1] - col_index)
                    black_count += 1
                elif col == Marble.WHITE:
                    white_dist += abs(mid_index[0] - row_index) + abs(mid_index[1] - col_index)
                    white_count += 1

        if white_count != 0:
            avg_white_dist = white_dist / white_count
        else:
            avg_white_dist = 0

        if black_count != 0:
            avg_black_dist = black_dist / black_count
        else:
            avg_black_dist = 0

    @classmethod
    def evaluation(cls, state):
        # How close to center of board are you?
        # How close to edge is opponent's pieces?
        # How clustered are the pieces?
        # Weight and features
        pass
