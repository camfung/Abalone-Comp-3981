from app.api.enums import Marble, Direction
from app.players.agent import AbaloneAgent

"""
To Be Implemented in Part 3.
"""


class AgentJoey(AbaloneAgent):
    """
    A sample agent created by Joey (A01320740) to calculate Evaluation Function.
    """

    @classmethod
    def evaluation(cls, state):
        """
        Base Evaluation Function for Agent which calls all other evaluation functions.
        :param state: GameState
        :return: integer representing the current evaluation value.
        """
        # Get Board State and Marble Positions on Board
        board = state.get_board()
        black_positions, white_positions = cls.find_positions_of_pieces(board)

        # List of Weights on Heuristic Functions
        weights = [50, 5, 5, 5]

        # Call Reward Functions to Calculate Toward Reward
        total_reward = cls.number_of_pieces(state, weights[0])
        total_reward += cls.grouped_together(board, black_positions, white_positions, weights[1])
        total_reward += cls.center_of_board(black_positions, white_positions, weights[2])
        total_reward += cls.anchored_pieces(board, black_positions, white_positions, weights[3])

        return total_reward

    @classmethod
    def find_positions_of_pieces(cls, board):
        """
        Find positions of all pieces on board.
        Possibly implemented into GameState instead of this Agent to be stored in GameState.

        :param board: Array Representation of GameState Board
        :return: Tuple containing List of Black Positions and White Positions
        """
        black_positions = []
        white_positions = []

        # Loop through every spot on the board.
        for rIndex, row in enumerate(board):
            for cIndex, col in enumerate(row):
                if col == Marble.BLACK:
                    black_positions.append([rIndex, cIndex])
                elif col == Marble.WHITE:
                    white_positions.append([rIndex, cIndex])

        return black_positions, white_positions

    @classmethod
    def number_of_pieces(cls, state, weight):
        """
        Heavily Reward Players for having more Pieces on the board.

        :param state: GameState
        :param weight: int representing the weight in evaluation
        :return: int value indicating total reward
        """
        pieces = state.get_ball_count()

        # Add up all white's pieces
        total_reward = (pieces[0] * -1)

        # Add up all black's pieces
        total_reward += pieces[1]

        return total_reward * weight

    @classmethod
    def grouped_together(cls, board, black_positions, white_positions, weight):
        """
        Reward Sides for Grouping Together.

        :param board: Array Representation of GameState Board
        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
        :param weight: int representing the weight in evaluation
        :return: int value indicating total reward
        """
        total_reward = 0

        # Calculate Black's Reward
        for black_position in black_positions:
            for direction in Direction:
                pos_x = black_position[0]
                pos_y = black_position[1]
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                for i in range(1, 3):
                    try:
                        if board[pos_x + (dir_x * i)][pos_y + (dir_y * i)] == Marble.BLACK:
                            total_reward += i
                    except IndexError:
                        continue

        # Calculate White's Reward
        for white_position in white_positions:
            for direction in Direction:
                pos_x = white_position[0]
                pos_y = white_position[1]
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                for i in range(1, 3):
                    try:
                        if board[pos_x + (dir_x * i)][pos_y + (dir_y * i)] == Marble.WHITE:
                            total_reward -= i
                    except IndexError:
                        continue

        return total_reward * weight

    @classmethod
    def center_of_board(cls, black_positions, white_positions, weight):
        """
        Reward Players for having pieces at Center of Board

        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
        :param weight: int representing the weight in evaluation
        :return: int value indicating total reward
        """
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

        return total_reward * weight

    @classmethod
    def anchored_pieces(cls, board, black_positions, white_positions, weight):
        """
        Punish Players for having single pieces close to being surrounded or is completely by opposing pieces

        :param board: Array Representation of GameState Board
        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
        :param weight: int representing the weight in evaluation
        :return: int value indicating total reward
        """
        total_reward = 0

        # Calculate Black's Punishment
        for black_position in black_positions:
            pos_x = black_position[0]
            pos_y = black_position[1]

            pieces_surrounded = 0

            # Check for All 6 Directions
            for direction in Direction:
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.WHITE:
                    pieces_surrounded += 1

            if pieces_surrounded > 4:
                total_reward -= pieces_surrounded

        # Calculate White's Punishment
        for white_position in white_positions:
            pos_x = white_position[0]
            pos_y = white_position[1]

            pieces_surrounded = 0

            # Check for All 6 Directions
            for direction in Direction:
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                if board[pos_x + dir_x][pos_y + dir_y] == Marble.BLACK:
                    pieces_surrounded += 1

            if pieces_surrounded > 4:
                total_reward += pieces_surrounded

        return total_reward * weight
