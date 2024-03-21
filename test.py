import csv
import unittest
from app.api.enums import Direction, Formation, Marble
from app.api.exceptions import InvalidMarbleValue
from app.api.filescriber import FileScriber
from collections import Counter

from app.gameplay.game import Game
from app.gameplay.game_state import GameState
from app.gameplay.move import Move


def getBoardState(board_spots, current_player):
    board_spots = board_spots.split(",")

    file = open('app/formations/blank_board.csv', 'r')
    csv_reader = csv.reader(file, delimiter=',')

    starting_board = [[None, None, None, None,
                       None, None, None, None, None, None, None]]

    for row in csv_reader:
        formatted_row = []
        for item in row:
            if item in "None":
                formatted_row.append(None)
            elif item in "EMPTY":
                formatted_row.append(Marble.NONE)
            else:
                raise InvalidMarbleValue(
                    f"{item} is not a valid marble value.")
        starting_board.append(formatted_row)

    starting_board.append(
        [None, None, None, None, None, None, None, None, None, None, None])

    file.close()

    for board_spot in board_spots:
        int_val = ord(board_spot[0])
        row = (int_val - 74) * -1
        col = int(board_spot[1])
        r_marble = board_spot[2]
        if r_marble == "b":
            marble = Marble.BLACK
        elif r_marble == "w":
            marble = Marble.WHITE
        starting_board[row][col] = marble

    # Step 4: Create New GameState from the Board Configuration (Step 3) & Current Player's Turn (Step 2)
    start_state = GameState(starting_board, current_player)
    return start_state


def getBoardStateFromFile(input_file):
    # Step 1: Read Input File
    with open(input_file, "r") as input_f:
        # Step 2: Read Current Player's Turn
        r_current_player = input_f.readline().strip()
        if r_current_player == "b":
            current_player = Marble.BLACK
        elif r_current_player == "w":
            current_player = Marble.WHITE

        # Step 3: Read Board Configuration
        r_board_config = input_f.readline().strip()
        board_spots = r_board_config.split(",")

        file = open('app/formations/blank_board.csv', 'r')
        csv_reader = csv.reader(file, delimiter=',')

        starting_board = [[None, None, None, None,
                           None, None, None, None, None, None, None]]

        for row in csv_reader:
            formatted_row = []
            for item in row:
                if item in "None":
                    formatted_row.append(None)
                elif item in "EMPTY":
                    formatted_row.append(Marble.NONE)
                else:
                    raise InvalidMarbleValue(
                        f"{item} is not a valid marble value.")
            starting_board.append(formatted_row)

        starting_board.append(
            [None, None, None, None, None, None, None, None, None, None, None])

        file.close()

        for board_spot in board_spots:
            int_val = ord(board_spot[0])
            row = (int_val - 74) * -1
            col = int(board_spot[1])
            r_marble = board_spot[2]
            if r_marble == "b":
                marble = Marble.BLACK
            elif r_marble == "w":
                marble = Marble.WHITE
            starting_board[row][col] = marble

    # Step 4: Create New GameState from the Board Configuration (Step 3) & Current Player's Turn (Step 2)
    start_state = GameState(starting_board, current_player)
    return start_state


def convert_to_string(coords):
    # Mapping of numbers to letters, where index 0 corresponds to 'I' and so forth

    num_to_letter = 'IHGFEDCBA'
    # Convert each coordinate tuple into its string representation
    result = []
    for coord in coords:
        # Convert the first element of the tuple from number to letter
        # Subtract 1 because the mapping starts from 1 but indexing starts from 0
        letter = num_to_letter[coord[0] - 1]
        # Combine the letter with the second element of the tuple, which remains unchanged
        result.append(f"({letter}{coord[1]})")

    # Join all the converted coordinates into a single string
    return ','.join(result)


def main():
    gameState = getBoardStateFromFile(
        "test/player/state_space_test/Input/Test1.input")

    # gameState = Game(Formation.DEFAULT).get_current_game_state()

    # print(gameState)
    # a = gameState.generate_own_marble_lines()
    # for line in a:
    #     print(convert_to_string(line))
    # move = Move((9, 5), (7, 5), Direction.UP_LEFT, Marble.BLACK)
    # a = gameState.validate_move(move)
    # print(a)
    moves = gameState.get_possible_moves()
    for move in moves:
        print(move.move_notation_str())
    print(len(moves))

    # a = gameState.line_to_edge((6, 3), Direction.UP_LEFT)
    # print(a)


def viewAllBoards():
    with open("/home/camer/Documents/projects/Abalone-Comp-3981/test/player/state_space_test/Verify/Test1.board") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            line = line.strip()
            a = getBoardState(line, Marble.BLACK)
            print(a)
            print(index)


viewAllBoards()
