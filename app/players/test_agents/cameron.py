from ast import Dict, List, Tuple
from app.api.enums import Marble
from app.gameplay.game_state import GameState
from app.players.agent import AbaloneAgent


class AgentCameron(AbaloneAgent):

    @staticmethod
    def extract_marbles(board):
        marbles = {}
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] is not None and board[row][col] != Marble.NONE:
                    marbles[(row, col)] = board[row][col]
        return marbles

    def calculate_manhattan_distance_to_center(self, marbles):
        distance_map = [
            [None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, 4, 4, 4, 4, 4, None],
            [None, None, None, None, 4, 3, 3, 3, 3, 4, None],
            [None, None, None, 4, 3, 2, 2, 2, 3, 4, None],
            [None, None, 4, 3, 2, 1, 1, 2, 3, 4, None],
            [None, 4, 2, 2, 1, 0, 1, 2, 3, 4, None],
            [None, 4, 3, 2, 1, 1, 2, 3, 4, None, None],
            [None, 4, 3, 2, 2, 2, 3, 4, None, None, None],
            [None, 4, 3, 2, 2, 3, 4, None, None, None, None],
            [None, 4, 4, 4, 4, 4, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None]
        ]
        center_position = (5, 5)  # E5 in the given board representation
        white_distance_sum = 0
        black_distance_sum = 0

        for position, color in marbles.items():
            # Calculate Manhattan distance for each marble to the center
            distance = distance_map[position[0]][position[1]]

            # Aggregate distances based on color
            if color == Marble.WHITE:
                white_distance_sum += distance
            else:  # Assuming any non-WHITE is BLACK for simplicity
                black_distance_sum += distance

        # Return the difference in total distances
        return white_distance_sum - black_distance_sum

    def calculate_cohesion(self, board_dict):
        # Neighbor offsets for even and odd rows
        even_row_neighbors = [(1, 0), (1, -1), (0, -1),
                              (-1, -1), (-1, 0), (0, 1)]
        odd_row_neighbors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (0, -1)]

        # Function to get neighbors based on row parity
        def get_neighbors(row: int, col: int):
            if row % 2 == 0:
                return [(row + dr, col + dc) for dr, dc in even_row_neighbors]
            else:
                return [(row + dr, col + dc) for dr, dc in odd_row_neighbors]

        # Counters for each team's cohesion
        white_cohesion, black_cohesion = 0, 0

        for (row, col), marble in board_dict.items():
            neighbors = get_neighbors(row, col)
            for n_row, n_col in neighbors:
                if (n_row, n_col) in board_dict and board_dict[(n_row, n_col)] == marble:
                    if marble == Marble.WHITE:
                        white_cohesion += 1
                    else:
                        black_cohesion += 1

        # Cohesion difference: WHITE's cohesion minus BLACK's cohesion
        if self.color == Marble.BLACK:
            return white_cohesion - black_cohesion
        return black_cohesion - white_cohesion

    def calculate_opponent_disruption(self, game_manager):
        return 0

    def evaluation(self, state: GameState):
        board_dict = self.extract_marbles(state._board)
        for (row, col), marble in board_dict.items():
            if marble == Marble.WHITE:
                board_dict[(row, col)] = Marble.NONE
        marble_cohesion = self.calculate_cohesion(board_dict)
        distance_to_center = self.calculate_manhattan_distance_to_center(
            board_dict)

        score = distance_to_center
        # print("========================================================")
        # print("score", score)
        # print(state)
        # print()

        return score
