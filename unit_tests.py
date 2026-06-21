import unittest

import numpy as np

from sudoku import Sudoku


class TestSudoku(unittest.TestCase):

    def test_is_solved(self):
        solved = np.load("reference-0.npy")
        self.assertTrue(Sudoku(solved).is_solved())

        # mess up the first row
        not_solved = solved.copy()
        not_solved[0, 0] = not_solved[0, 1]
        s = Sudoku(not_solved)
        self.assertFalse(s.is_solved())
        self.assertFalse(s.check_rows())

        # mess up the first column
        not_solved = solved.copy()
        not_solved[0, 0] = not_solved[1, 0]
        s = Sudoku(not_solved)
        self.assertFalse(s.is_solved())
        self.assertFalse(s.check_cols())

        # mess up the last box
        not_solved = solved.copy()
        not_solved[8, 8] = not_solved[6, 6]
        s = Sudoku(not_solved)
        self.assertFalse(s.is_solved())
        self.assertFalse(s.check_boxes())

        # any value not in the range 1-9 should be ignored
        not_solved = solved.copy()
        not_solved[0, 0] = 10
        self.assertFalse(Sudoku(not_solved).is_solved())


if __name__ == "__main__":
    unittest.main()
