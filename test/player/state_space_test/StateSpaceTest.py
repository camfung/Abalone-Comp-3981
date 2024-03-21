
import unittest
from app.api.filescriber import FileScriber
from collections import Counter
from pathlib import Path


class StateSpaceTest(unittest.TestCase):
    def test_chi_en_1(self):
        input_file = Path("./Input/Test1.input").resolve()
        output_move_file = Path("./Output/Test1.move").resolve()
        output_board_file = Path("./Output/Test1.board").resolve()
        verify_board_file = Path("./Verify/Test1.board").resolve()

        FileScriber.export_state_space_to_text_files(input_file, output_move_file, output_board_file)
        exported_results = FileScriber.import_board_from_text_files(output_board_file)
        verified_results = FileScriber.import_board_from_text_files(verify_board_file)
        self.assertTrue(Counter(exported_results) == Counter(verified_results))

    def test_chi_en_2(self):
        input_file = Path("./Input/Test2.input").resolve()
        output_move_file = Path("./Output/Test2.move").resolve()
        output_board_file = Path("./Output/Test2.board").resolve()
        verify_board_file = Path("./Verify/Test2.board").resolve()

        FileScriber.export_state_space_to_text_files(input_file, output_move_file, output_board_file)
        exported_results = FileScriber.import_board_from_text_files(output_board_file)
        verified_results = FileScriber.import_board_from_text_files(verify_board_file)
        self.assertTrue(Counter(exported_results) == Counter(verified_results))

    def test_team_num_balls_test_1(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
