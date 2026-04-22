from ast import Dict, List, Tuple
from app.api.enums import Direction, Marble
from app.gameplay.game_state import GameState
from app.players.agent import AbaloneAgent


class AgentCameron(AbaloneAgent):

    @staticmethod
    def get_board_dict(board):
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
            [None, 4, 3, 2, 1, 0, 1, 2, 3, 4, None],
            [None, 4, 3, 2, 1, 1, 2, 3, 4, None, None],
            [None, 4, 3, 2, 2, 2, 3, 4, None, None, None],
            [None, 4, 3, 3, 3, 3, 4, None, None, None, None],
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

    def get_neighbor(self, pos, direction):
        """
        Get the neighbor of a position in a given direction
        :param pos: The position of the marble
        :param direction: The direction to check
        :return: The position of the neighbor
        """
        row, col = pos
        # check if it is in bounds
        if row < 1 or row >= 10 or col < 1 or col >= 10:
            return None
        if direction == Direction.UP_LEFT:
            return row - 1, col
        elif direction == Direction.UP_RIGHT:
            return row - 1, col + 1
        elif direction == Direction.RIGHT:
            return row, col + 1
        elif direction == Direction.DOWN_RIGHT:
            return row + 1, col
        elif direction == Direction.DOWN_LEFT:
            return row + 1, col - 1
        elif direction == Direction.LEFT:
            return row, col - 1

    def calculate_cohesion(self, board_dict):
        # Counters for each team's cohesion
        white_cohesion, black_cohesion = 0, 0

        for pos, color in board_dict.items():
            if color == Marble.WHITE:
                for direction in Direction:
                    neighbor = self.get_neighbor(pos, direction)
                    if neighbor in board_dict and board_dict[neighbor] == Marble.WHITE:
                        print("current", pos, "neighbor", neighbor)
                        white_cohesion += 1
                    print(white_cohesion)
            else:
                for direction in Direction:
                    neighbor = self.get_neighbor(pos, direction)
                    print("current", pos, "neighbor", neighbor)
                    if neighbor in board_dict and board_dict[neighbor] == Marble.BLACK:
                        black_cohesion += 1
                    print(black_cohesion)

        # Cohesion difference: WHITE's cohesion minus BLACK's cohesion
        if self.color == Marble.BLACK:
            return white_cohesion - black_cohesion
        return black_cohesion - white_cohesion

    def calculate_opponent_disruption(self, game_manager):
        return 0

    def evaluation(self, state: GameState):
        board_dict = self.get_board_dict(state._board)
        for (row, col), marble in board_dict.items():
            if marble == Marble.WHITE:
                board_dict[(row, col)] = Marble.NONE
        marble_cohesion = self.calculate_cohesion(board_dict)
        distance_to_center = self.calculate_manhattan_distance_to_center(
            board_dict)

        score = distance_to_center + marble_cohesion
        # print("========================================================")
        # print("score", score)
        # print(state)
        # print()

        return score
