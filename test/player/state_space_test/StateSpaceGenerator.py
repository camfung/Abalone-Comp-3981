import os
from filescriber import FileScriber


class FileProcessor:
    def run_test(self, folder_path):
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a valid directory.")
            return

        output_number = 1

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            output_move_file = f"Output_Move{output_number}.move"
            output_board_file = f"Output_Board{output_number}.board"

            if os.path.isfile(file_path):
                with open(output_move_file, 'w') as move_file, \
                        open(output_board_file, 'w') as board_file:
                    FileScriber.export_state_space_to_text_files(file_path, move_file, board_file)

                output_number += 1


if __name__ == "__main__":
    processor = FileProcessor()
    folder_path = "./Output/"
    processor.run_test(folder_path)
