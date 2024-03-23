from app.api.enums import Marble, Direction
from app.players.agent import AbaloneAgent

"""
To Be Implemented in Part 3.
"""


class AgentJoey(AbaloneAgent):
    @classmethod
    def evaluation(cls, state):
        board = state.get_board()
        pieces = state.get_ball_count()
        black_positions, white_positions = cls.find_positions_of_pieces(board)

        # Add up all white's pieces
        total_reward = pieces[0] * -1

        # Add up all black's pieces
        total_reward += pieces[1]

        total_reward += cls.grouped_together(board, black_positions, white_positions)
        total_reward += cls.center_of_board(board, black_positions, white_positions)
        total_reward += cls.anchored_pieces(board, black_positions, white_positions)

        return total_reward

    @classmethod
    def find_positions_of_pieces(cls, board):
        black_positions = []
        white_positions = []

        for rIndex, row in enumerate(board):
            for cIndex, col in enumerate(row):
                if col == Marble.BLACK:
                    black_positions.append([rIndex, cIndex])
                elif col == Marble.WHITE:
                    white_positions.append([rIndex, cIndex])

        return black_positions, white_positions

    @classmethod
    def grouped_together(cls, board, black_positions, white_positions):
        total_reward = 0

        for black_position in black_positions:
            for direction in Direction:
                pos_x = black_position[0]
                pos_y = black_position[1]
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.BLACK:
                    total_reward += 1

        for white_position in white_positions:
            for direction in Direction:
                pos_x = white_position[0]
                pos_y = white_position[1]
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.WHITE:
                    total_reward -= 1

        return total_reward

    @classmethod
    def center_of_board(cls, board, black_positions, white_positions):
        total_reward = 0
        center_board = (5, 5)

        # Calculate Black's Reward
        for black_position in black_positions:
            pos_x = black_position[0]
            pos_y = black_position[1]

            dist_x = abs(center_board[0] - pos_x)
            dist_y = abs(center_board[1] - pos_y)
            black_distance = max(dist_x, dist_y)

            total_reward -= black_distance

        # Calculate White's Reward
        for white_position in white_positions:
            pos_x = white_position[0]
            pos_y = white_position[1]

            dist_x = abs(center_board[0] - pos_x)
            dist_y = abs(center_board[1] - pos_y)
            white_distance = max(dist_x, dist_y)

            total_reward += white_distance

        return total_reward

    @classmethod
    def anchored_pieces(cls, board, black_positions, white_positions):
        total_reward = 0

        for black_position in black_positions:
            pos_x = black_position[0]
            pos_y = black_position[1]

            # Check for All 6 Directions
            for direction in Direction:
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.WHITE:
                    total_reward -= 1

        for white_position in white_positions:
            pos_x = white_position[0]
            pos_y = white_position[1]

            for direction in Direction:
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.BLACK:
                    total_reward -= 1

        return total_reward
