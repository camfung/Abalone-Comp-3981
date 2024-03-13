
from app.gameplay.game_state import GameState
from app.api.enums import Marble


class FileScriber:
    @staticmethod
    def export_state_space_to_text_files(input_file, output_move_file, output_board_file):
        # Step 1: Read Input File
        with open(input_file, "r") as input_f:
            # Step 2: Read Current Player's Turn
            r_current_player = input_f.readline()
            if r_current_player == "b":
                current_player = Marble.BLACK
            elif r_current_player == "w":
                current_player = Marble.WHITE

            # Step 3: Read Board Configuration
            r_board_config = input_f.readline()
            board_spots = r_board_config.split(",")

            starting_board = []
            for i in range(0, 11):
                starting_board.append(
                    [None, None, None, None, None, None, None, None, None, None, None])

            for board_spot in board_spots:
                int_val = int(board_spot[0])
                row = int_val - 74 + 2 * (int_val - 64)
                col = int(board_spot[1])
                r_marble = board_spot[2]
                if r_marble == "b":
                    marble = Marble.BLACK
                elif r_marble == "w":
                    marble = Marble.WHITE
                starting_board[row][col] = marble

        # Step 4: Create New GameState from the Board Configuration (Step 3) & Current Player's Turn (Step 2)
        start_state = GameState(starting_board, marble)

        # Step 5: Get GameState's State Space Generation (List of Moves & Boards)
        all_moves = start_state.get_possible_moves()
        all_boards = start_state.convert_moves_to_board_states()

        # Step 6: Export List of Moves to Output Move File
        with open(output_move_file, "w") as output_f:
            for move in all_moves:
                output_f.write(move)

        # Step 7: Export List of Boards to Output Board File
        with open(output_board_file, "w") as output_f:
            for board in all_boards:
                spaces = []
                for rIndex, row in enumerate(board):
                    for cIndex, col in enumerate(row):
                        str_row = f"{chr(rIndex)}"

                        if col is None or col == Marble.NONE:
                            continue
                        elif col == Marble.BLACK:

                            formatted_space = f"{cIndex}b"
                            spaces.append(formatted_space)
                        elif col == Marble.BLACK:
                            formatted_space = f"{cIndex}w"
                            spaces.append(formatted_space)

    @staticmethod
    def import_board_from_text_files(input_file):
        # Read Board File

        # Return Results
        pass

