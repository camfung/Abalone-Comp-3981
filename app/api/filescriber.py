from app.api.exceptions import InvalidMarbleValue
from app.gameplay.game_state import GameState
from app.api.enums import Marble
import csv


class FileScriber:
    @staticmethod
    def export_state_space_to_text_files(input_file, output_move_file, output_board_file):
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

            file = open('../../../app/formations/blank_board.csv', 'r')
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

            char_board = {
                # Row on Board: Char Value
                'I': 1,
                'H': 2,
                'G': 3,
                'F': 4,
                'E': 5,
                'D': 6,
                'C': 7,
                'B': 8,
                'A': 9
            }

            for board_spot in board_spots:
                row = char_board[board_spot[0]]
                col = int(board_spot[1])
                r_marble = board_spot[2]
                if r_marble == "b":
                    marble = Marble.BLACK
                elif r_marble == "w":
                    marble = Marble.WHITE
                starting_board[row][col] = marble

        # Step 4: Create New GameState from the Board Configuration (Step 3) & Current Player's Turn (Step 2)
        start_state = GameState(starting_board, current_player)

        # Step 5: Get GameState's State Space Generation (List of Moves & Boards)
        all_moves = start_state.get_possible_moves()
        all_boards = start_state.convert_moves_to_board_states()

        # Step 6: Export List of Moves to Output Move File
        with open(output_move_file, "w") as output_f:
            for move in all_moves:
                output_f.write(f"{move.move_notation_str()}\n")

        int_to_char_board = {v: k for k, v in char_board.items()}

        # Step 7: Order List to Chi En's standard
        board_positions = []
        for board in all_boards:
            spaces = ""
            # Iterate through rows in reverse order
            for rIndex in range(len(board) - 1, -1, -1):
                row = board[rIndex]
                for cIndex, col in enumerate(row):
                    try:
                        row_key = int_to_char_board[rIndex]
                        str_row = f"{row_key}"
                    except KeyError:
                        continue
                    if col is None or col == Marble.NONE:
                        continue
                    elif col == Marble.BLACK:
                        formatted_space = f"{str_row}{cIndex}b"
                        spaces += f"{formatted_space},"
                    elif col == Marble.WHITE:
                        formatted_space = f"{str_row}{cIndex}w"
                        spaces += f"{formatted_space},"
            spaces = spaces.rstrip(',')
            spaces_list = spaces.split(',')
            spaces_list = sorted(spaces_list, key=lambda x: (x[2], x[0], x[1]))
            board_positions.append(spaces_list)

        # Step 8: Export List of Boards to Output Board File
        with open(output_board_file, "w") as output_f:
            for position in board_positions:
                formation = ""
                for piece in position:
                    formation += f"{piece},"
                formation = formation.rstrip(',')
                formation += "\n"
                output_f.writelines(formation)

    @staticmethod
    def import_board_from_text_files(input_file):
        # Read Board File
        with open(input_file, "r") as input_f:
            lines = input_f.readlines()
            print(lines)

        # Return Results
        return lines

