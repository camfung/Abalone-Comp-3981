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
        moves = game_manager.get_current_game_state().get_possible_moves()
        board = game_manager.get_current_game_state().get_board()


        # move_to_make = self.move_to_center(game_manager.get_current_game_state().get_possible_moves())
        push_move = self.push_pieces(moves, board)

        move_to_make = self.move_away_edge(game_manager.get_current_game_state().get_possible_moves())

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

    def move_to_center(self, moves):
        best_move_pos = (10, 10)  # Pick a position off the board
        best_move_str = ""
        best_move = None

        for move in moves:
            if self.calc_single_middle_dist(move.get_pos_f()[0]) < self.calc_single_middle_dist(best_move_pos):
                best_move_pos = move.get_pos_f()[0]
                best_move_str = str(move)
                best_move = move
                print(f"current best move is {move.get_pos_i()} {move.get_pos_f()} {best_move_pos} {best_move_str} "
                      f"{move.get_marble()}")

        print(str(f"best move is {best_move_str} {best_move_str}"))
        return best_move

    def move_away_edge(self, moves):
        best_move_pos = (10, 10)  # Pick a position off the board
        best_move_str = ""
        best_move = None
        best_horizontal_move = None

        for move in moves:

            if self.calc_single_edge_dist(move.get_pos_f()[1]) <= self.calc_single_edge_dist(best_move_pos):
                if move.get_direction() != Direction.LEFT and move.get_direction() != Direction.RIGHT:
                    dist_to_edge = self.calc_single_edge_dist(best_move_pos)
                    best_move_pos = move.get_pos_f()[1]
                    best_move_str = str(move)
                    best_move = move
                    print(f"current best move is {best_move_str} dist to edge {dist_to_edge} {move.get_direction()}")
                else:
                    best_horizontal_move = move
            else:
                continue

        if best_horizontal_move is not None:
            best_move = best_horizontal_move
            print("go sideways")

        if best_move is None: #Prevent returning none for now
            return random.choice(moves)

        print(str(f"best move is {best_move_str}"))
        return best_move

    def push_pieces(self, moves, board):
        best_move = None
        opponent_marbles = []

        if self.color == Marble.BLACK:
            opponent_colour = Marble.WHITE
        else:
            opponent_colour = Marble.BLACK

        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if board[row_index][col_index] == opponent_colour:
                    pos_tuple = (row_index, col_index)
                    opponent_marbles.append(pos_tuple)

        for move in moves:
            for pos in opponent_marbles:
                if move.get_pos_f()[0] == pos:
                    best_move = move

        if best_move is not None:
            return best_move

    @classmethod
    def evaluation(cls, state):
        # How close to center of board are you?
        # How close to edge is opponent's pieces?
        # How clustered are the pieces?
        # Weight and features
        pass
