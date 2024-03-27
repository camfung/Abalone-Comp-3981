import timer as timer

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
    def make_move(self, game_manager: GameManager, player: Marble, move: Move, timestamp: float) -> None:
        """
        Commits a move made by the AI agent to the game manager, simulating a delay before making the move.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        - time_stamp: The timestamp when the move was generated.
        """
        move_to_make = self.move_to_center(game_manager.get_current_game_state().get_possible_moves())
        game_manager.commit_move(player, move_to_make, timestamp)

    @staticmethod
    def calc_single_distance(coord):
        """
        Calculates the distance of a single marble from the center of the board
        """
        center = (5, 5)
        return abs(coord[0] - center[0]) + abs(coord[1] - center[1])

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

    @staticmethod
    def move_to_center(self, moves):
        best_move_pos = (10, 10)  # Pick a position off the board
        best_move_str = ""
        best_move = None

        for move in moves:
            if self.calc_single_distance(move.get_pos_f()[0]) < self.calc_single_distance(best_move_pos):
                best_move_pos = move.get_pos_f()[0]
                best_move_str = str(move)
                best_move = move
                print(f"current best move is {move.get_pos_i()} {move.get_pos_f()} {best_move_pos} {best_move_str} "
                      f"{move.get_marble()}")

        print(str(f"best move is {best_move_str} {best_move_str}"))
        return best_move

    @classmethod
    def evaluation(cls, state):
        # How close to center of board are you?
        # How close to edge is opponent's pieces?
        # How clustered are the pieces?
        # Weight and features
        pass
