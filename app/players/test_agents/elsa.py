from app.players.agent import AbaloneAgent

import datetime
import random
import time
from app.communication.game_manager import GameManager
from app.api.enums import Marble, Direction
from app.gameplay.move import Move


class AgentElsa(AbaloneAgent):
    def generate_move(self, game_manager, timer):  # Placeholder until generate_move gets fixed
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

    def make_move(self, game_manager: GameManager, player: Marble, move: Move, timestamp: float) -> None:
        """
        Commits a move made by the AI agent to the game manager, simulating a delay before making the move.

        Parameters:
        - game_manager: The GameManager instance managing the game state.
        - player: The color of the player making the move.
        - move: The Move object representing the move to be made.
        - time_stamp: The timestamp when the move was generated.
        """
        self.evaluation(game_manager.get_current_game_state())
        moves = game_manager.get_current_game_state().generate_possible_moves()
        board = game_manager.get_current_game_state().get_board()

        push_move = self.push_pieces(moves, board)
        move_to_make = self.move_to_center(game_manager.get_current_game_state().generate_possible_moves())
        # move_to_make = self.move_away_edge(game_manager.get_current_game_state().generate_possible_moves())

        if push_move is not None:
            move_to_make = push_move

        game_manager.commit_move(player, move_to_make, timestamp)

    @staticmethod
    def calc_single_middle_dist(coord):
        """
        Calculates the distance of a single marble from the center of the board
        """
        center = (5, 5)
        return abs(coord[0] - center[0]) + abs(coord[1] - center[1])

    @staticmethod
    def calc_single_edge_dist(coord):
        x, y = coord[0], coord[1]

        edge_x = 1 if x <= 5 else 9

        if y < 6:
            edge_y = 1 if x < 6 else 2 if x == 6 else 3 if x == 7 else 4 if x == 8 else 5
        else:
            edge_y = 9 if x > 4 else 8 if x == 4 else 7 if x == 3 else 6 if x == 2 else 1

        return abs(x - edge_x) + abs(y - edge_y)

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

            edge_x = 1 if x <= 5 else 9

            if y < 6:
                edge_y = 1 if x < 6 else 2 if x == 6 else 3 if x == 7 else 4 if x == 8 else 5
            else:
                edge_y = 9 if x > 4 else 8 if x == 4 else 7 if x == 3 else 6 if x == 2 else 1

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
                    print(f"Black edge dist is {black_edge_dist}")
                elif col == Marble.WHITE:
                    white_edge_dist += calc_single_edge_dist((row_index, col_index))
                    white_count += 1
                    print(f"Black edge dist is {white_edge_dist}")

        if white_count != 0:
            avg_white_edge_dist = white_edge_dist / white_count
        else:
            avg_white_edge_dist = 0

        if black_count != 0:
            avg_black_edge_dist = black_edge_dist / black_count
        else:
            avg_black_edge_dist = 0

        print(f"White edge dist {avg_white_edge_dist} Black edge dist {avg_black_edge_dist}")
        return avg_black_edge_dist - avg_white_edge_dist

    def move_to_center(self, moves):
        best_move = None
        best_distance_to_center = float('inf')

        for move in moves:
            pos = move.get_pos_f()[0]
            distance_to_center = self.calc_single_middle_dist(pos)

            if distance_to_center < best_distance_to_center:
                best_move = move
                best_distance_to_center = distance_to_center

        return best_move

    def move_away_edge(self, moves):
        best_move = None
        best_distance_to_edge = float('inf')

        for move in moves:
            pos = move.get_pos_f()[1]
            direction = move.get_direction()

            if (direction == Direction.LEFT or direction == Direction.RIGHT) and pos[1] < best_distance_to_edge:
                best_move = move
                best_distance_to_edge = pos[1]
            elif direction != Direction.LEFT and direction != Direction.RIGHT:
                distance_to_edge = self.calc_single_edge_dist(pos)
                if distance_to_edge < best_distance_to_edge:
                    best_move = move
                    best_distance_to_edge = distance_to_edge

        if best_move is None:
            return random.choice(moves)

        return best_move

    def push_pieces(self, moves, board):
        best_move = None
        opponent_marbles = set()

        if self.color == Marble.BLACK:
            opponent_colour = Marble.WHITE
        else:
            opponent_colour = Marble.BLACK

        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if col == opponent_colour:
                    opponent_marbles.add((row_index, col_index))

        for move in moves:
            if move.get_pos_f()[0] in opponent_marbles:
                best_move = move
                break

        return best_move

    @classmethod
    def evaluation(cls, state):
        # How close to center of board are you?
        # How close to edge is opponent's pieces?
        # How clustered are the pieces?
        # Weight and features
        center_distance = cls.calc_center_distance(state)
        edge_distance = cls.calc_edge_distance(state)
        print(f"Center distance is {center_distance} Edge distance is {edge_distance}")
