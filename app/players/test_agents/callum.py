from app.api.enums import Marble
from app.players.agent import AbaloneAgent

"""
To Be Implemented in Part 3.
"""


class AgentCallum(AbaloneAgent):

    def evaluation(self, state):
        """
        Evaluate the current state based on heuristics.

        Heuristics will be implemented in Part 3.
        :param state: GameState
        :return: Evaluation Value as an integer.
        """
        ##Have move set to best move so far
        ##create methods to see how much together the BALLS are
        ##create method to see how far away from edge BALLS are
        ##go through valid moves, evaluate based on new methods, along with if the move reduces opponent
        ##ball count
        ##check if time is up, if it is return best move so far

        board = state._board
        bunch = self.evaluate_bunching(board)
        defensive = self.defensive_strength(board)
        pushes = self.potential_pushes(board)
        distance_edge = self.distance_from_edge(board)
        white_balls, black_balls = state.get_ball_count()

        if self.color == Marble.WHITE:
            self.balls = white_balls
            self.opponent_balls = black_balls
        else:
            self.balls = black_balls
            self.opponent_balls = white_balls

        return bunch + distance_edge + 180 * (self.balls - self.opponent_balls) + pushes + defensive


    def evaluate_bunching(self, board):
        bunching_scores = 0

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == self.color:
                    bunching_scores += self.count_neighbors(board, i, j)

        return bunching_scores

    def count_neighbors(self, board, x, y):
        neighbors = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue  # Skip the current position
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]) and board[new_x][new_y] == Marble.WHITE:
                    neighbors += 1
        return neighbors


    def distance_from_edge(self, board):
        distances = 0

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == self.color:
                    distance = abs(5 - i) + abs(5 - j)
                    distance =  max(0, 11 - distance)
                    distances += distance

        return distances

    def defensive_strength(self, board):
        strength = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == self.color:
                    # Check neighboring positions for opponent's presence
                    for d_row, d_col in [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1)]:
                        new_row, new_col = row + d_row, col + d_col
                        if 0 <= new_row < len(board) and 0 <= new_col < len(board[row]):
                            if board[new_row][new_col] != self.color and board[new_row][new_col] != None:
                                # If opponent is nearby, increase defensive strength
                                strength += 1
        return strength

    def potential_pushes(self, board):
        push_count = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == self.color:
                    # Check neighboring positions for potential pushes
                    for d_row, d_col in [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1)]:
                        new_row, new_col = row + d_row, col + d_col
                        if 0 <= new_row < len(board) and 0 <= new_col < len(board[row]):
                            # Check if neighboring position is occupied by opponent
                            if board[new_row][new_col] != self.color and board[new_row][new_col] != 0:
                                # Check if pushing in that direction is possible
                                next_row, next_col = new_row + d_row, new_col + d_col
                                if 0 <= next_row < len(board) and 0 <= next_col < len(board[row]):
                                    # Check if next position is empty or on the board
                                    if board[next_row][next_col] == 0:
                                        push_count += 1
        return push_count

