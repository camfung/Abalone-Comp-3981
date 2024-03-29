from app.api.enums import Marble, Direction
from app.players.agent import AbaloneAgent

"""
To Be Implemented in Part 3.
"""


class AgentJoey(AbaloneAgent):
    """
    A sample agent created by Joey (A01320740) to calculate Evaluation Function.
    """

    def evaluation(self, state, calculating_player):
        """
        Base Evaluation Function for Agent which calls all other evaluation functions.
        :param calculating_player: Marble that represents the player deciding move
        :param state: GameState
        :return: integer representing the current evaluation value.
        """
        # Get Board State and Marble Positions on Board
        board = state.get_board()
        black_positions, white_positions = self.find_positions_of_pieces(board)

        # Get Multiplier
        if calculating_player == Marble.BLACK:
            black_multiplier = 1
            white_multiplier = -1
        else:
            black_multiplier = -1
            white_multiplier = 1

        # List of Weights on Heuristic Functions
        if self._current_move < 6:
            weights = [100, 2, 5, 5]
        else:
            weights = [100, 5, 2, 5]

        # Call Reward Functions to Calculate Toward Reward
        total_reward = self.number_of_pieces(state, weights[0], white_multiplier, black_multiplier)
        total_reward += self.grouped_together(board, black_positions, white_positions, weights[1],
                                              white_multiplier, black_multiplier)
        total_reward += self.center_of_board(black_positions, white_positions, weights[2],
                                             white_multiplier, black_multiplier)
        # total_reward += self.anchored_pieces(board, black_positions, white_positions, weights[3],
        #                                     white_multiplier, black_multiplier)

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
    def number_of_pieces(cls, state, weight, white_multiplier, black_multiplier):
        """
        Heavily Reward Players for having more Pieces on the board.

        :param black_multiplier: 1 or -1
        :param white_multiplier: 1 or -1
        :param state: GameState
        :param weight: int representing the weight in evaluation
        :return: int value indicating total reward
        """
        pieces = state.get_ball_count()

        # Add up all white's pieces
        total_reward = pieces[0] * white_multiplier

        # Add up all black's pieces
        total_reward += pieces[1] * black_multiplier

        return total_reward * weight

    @classmethod
    def grouped_together(cls, board, black_positions, white_positions, weight, white_multiplier, black_multiplier):
        """
        Reward Sides for Grouping Together.

        :param black_multiplier: 1 or -1
        :param white_multiplier: 1 or -1
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
                            total_reward += i * black_multiplier
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
                            total_reward += i * white_multiplier
                    except IndexError:
                        continue

        return total_reward * weight

    @classmethod
    def center_of_board(cls, black_positions, white_positions, weight, white_multiplier, black_multiplier):
        """
        Reward Players for having pieces at Center of Board

        :param black_multiplier: 1 or -1
        :param white_multiplier: 1 or -1
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

            total_reward -= black_distance ** 2 * black_multiplier

        # Calculate White's Reward
        for white_position in white_positions:
            pos_x = white_position[0]
            pos_y = white_position[1]

            dist_x = abs(center_board[0] - pos_x)
            dist_y = abs(center_board[1] - pos_y)
            white_distance = max(dist_x, dist_y)

            total_reward -= white_distance ** 2 * white_multiplier

        return total_reward * weight

    @classmethod
    def anchored_pieces(cls, board, black_positions, white_positions, weight, white_multiplier, black_multiplier):
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
                total_reward -= pieces_surrounded * black_multiplier

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
                total_reward += pieces_surrounded * white_multiplier

        return total_reward * weight
