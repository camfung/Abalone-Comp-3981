

import unittest
from app.api.filescriber import FileScriber


class StateSpaceTest(unittest.TestCase):
    def test_chi_en_test_1(self):
        FileScriber.export_state_space_to_text_files("./Input/Test1.input",
                                                     "./Output/Test1.move",
                                                     "./Output/Test1.board")
        exported_results = FileScriber.import_board_from_text_files("./Output/Test1.board")
        verified_results = FileScriber.import_board_from_text_files("./Verify/Test1.board")
        self.assertEqual(sorted(exported_results), sorted(verified_results))

    def test_chi_en_test_2(self):
        FileScriber.export_state_space_to_text_files("./Input/Test2.input",
                                                     "./Output/Test2.move",
                                                     "./Output/Test2.board")
        exported_results = FileScriber.import_board_from_text_files("./Output/Test2.board")
        verified_results = FileScriber.import_board_from_text_files("./Verify/Test2.board")
        self.assertEqual(sorted(exported_results), sorted(verified_results))

    def test_team_num_balls_test_1(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
