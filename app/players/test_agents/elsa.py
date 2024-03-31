from app.players.agent import AbaloneAgent

import datetime
import random
import time
from app.communication.game_manager import GameManager
from app.api.enums import Marble, Direction
from app.gameplay.move import Move


class AgentElsa(AbaloneAgent):

    @staticmethod
    def calc_single_middle_dist(coord):
        """
        Calculates the distance of a single marble from the center of the board
        """
        center = (5, 5)
        return abs(coord[0] - center[0]) + abs(coord[1] - center[1])

    @staticmethod
    def calc_center_distance(state):
        """
        Calculates the distance from the center of the board and returns an evaluation.
        :param state: Gamestate
        :return: Double
        """
        board = state.get_board()
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

        return avg_white_dist - avg_black_dist

    @staticmethod
    def calc_edge_distance(state):
        """
        Calculates the average distance of each player's marbles from the edge of the board and returns an evaluation.
        :param state: Gamestate
        :return: Double
        """

        def calc_single_edge_dist(coord):
            x, y = coord[0], coord[1]

            edge_y = 1 if y <= 5 else 9

            if x < 6:
                edge_x = 1 if y < 6 else 2 if y == 6 else 3 if y == 7 else 4 if y == 8 else 5
            else:
                edge_x = 9 if y > 4 else 8 if y == 4 else 7 if y == 3 else 6 if y == 2 else 1

            return abs(x - edge_x) + abs(y - edge_y)

        board = state.get_board()
        white_edge_dist = 0
        black_edge_dist = 0
        white_count = 0
        black_count = 0

        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if col == Marble.BLACK:
                    black_edge_dist += calc_single_edge_dist((row_index, col_index))
                    black_count += 1
                elif col == Marble.WHITE:
                    white_edge_dist += calc_single_edge_dist((row_index, col_index))
                    white_count += 1

        if white_count != 0:
            avg_white_edge_dist = white_edge_dist / white_count
        else:
            avg_white_edge_dist = 0

        if black_count != 0:
            avg_black_edge_dist = black_edge_dist / black_count
        else:
            avg_black_edge_dist = 0

        return avg_white_edge_dist - avg_black_edge_dist

    @classmethod
    def evaluation(cls, state):
        center_distance = cls.calc_center_distance(state)
        edge_distance = cls.calc_edge_distance(state)

        weight = [25, 75]

        return (center_distance * weight[0]) + (edge_distance * weight[1])



