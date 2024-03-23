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
        total_reward += cls.center_of_board(black_positions, white_positions)
        total_reward += cls.anchored_pieces(board, black_positions, white_positions)

        return total_reward

    @classmethod
    def find_positions_of_pieces(cls, board):
        """
        Find positions of all pieces on board.
        Possibly implemented into GameState instead of Agent to be stored in GameState.
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
    def grouped_together(cls, board, black_positions, white_positions):
        """
        Reward Sides for Grouping Together.
        :param board: Array Representation of GameState Board
        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
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
                    if board[pos_x + (dir_x * i)][pos_y + (dir_y * i)] == Marble.BLACK:
                        total_reward += i

        # Calculate White's Reward
        for white_position in white_positions:
            for direction in Direction:
                pos_x = white_position[0]
                pos_y = white_position[1]
                dir_x = direction.value[0]
                dir_y = direction.value[1]

                for i in range(1, 3):
                    if board[pos_x + (dir_x * i)][pos_y + (dir_y * i)] == Marble.WHITE:
                        total_reward -= i

        return total_reward

    @classmethod
    def center_of_board(cls, black_positions, white_positions):
        """
        Reward Players for having pieces at Center of Board

        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
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

        return total_reward

    @classmethod
    def anchored_pieces(cls, board, black_positions, white_positions):
        """
        Punish Players for having single pieces close to being surrounded or is completely by opposing pieces

        :param board: Array Representation of GameState Board
        :param black_positions: List of Tuples representing Black Positions
        :param white_positions: List of Tuples representing White Positions
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
                total_reward -= (pieces_surrounded * 10)

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
                total_reward += (pieces_surrounded * 10)

        return total_reward
