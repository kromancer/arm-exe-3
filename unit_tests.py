import unittest

import numpy as np

from sudoku import Sudoku


class TestSudoku(unittest.TestCase):

    def test_is_solved(self):
        solved = np.load("reference-0.npy")
        self.assertTrue(Sudoku(solved).is_solved())

        # mess up the first row/column/box
        not_solved = solved.copy()
        not_solved[0, 0] = 0
        s = Sudoku(not_solved)
        self.assertFalse(s.is_solved())
        self.assertFalse(s.check_rows())
        self.assertFalse(s.check_cols())
        self.assertFalse(s.check_boxes())

    def test_propagate_assign(self):
        """
        Check that the propagation of constraints works correctly,
        and that we can solve trivial sudokus with just propagation + assignment
        """
        solved = np.load("reference-0.npy")

        def check_solve(grid):
            sudoku = Sudoku(grid)
            self.assertFalse(sudoku.is_solved())
            sudoku.solve()
            self.assertTrue(sudoku.is_solved())

        # remove an assignment from each row and check that the sudoku can be solved
        not_solved = solved.copy()
        not_solved[:, 0] = 0
        check_solve(not_solved)

        # remove an assignment from each column and check that the sudoku can be solved
        not_solved = solved.copy()
        not_solved[8, :] = 0
        check_solve(not_solved)

        # remove an assignment from each box and check that the sudoku can be solved
        not_solved = solved.copy()
        not_solved.reshape(3, 3, 3, 3).swapaxes(1, 2)[:, :, 0, 0] = 0
        check_solve(not_solved)

    def test_validate_input_grid(self):
        invalid = np.load("input-3.npy")
        with self.assertRaises(ValueError):
            _ = Sudoku(invalid)

    def test_backtracking(self):
        grid = np.array(
            [
                [0, 3, 0, 0, 0, 7, 2, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 5],
                [6, 0, 0, 8, 0, 0, 4, 0, 3],
                [0, 0, 3, 0, 9, 5, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 2, 1, 0, 6, 0, 0],
                [7, 0, 5, 0, 0, 6, 0, 0, 2],
                [2, 0, 0, 0, 0, 0, 0, 0, 7],
                [0, 0, 1, 4, 0, 0, 0, 9, 0]
            ]
        )

        s = Sudoku(grid)
        s.solve()
        self.assertTrue(s.is_solved())

        solution = np.array(
            [
                [9, 3, 4, 1, 5, 7, 2, 6, 8],
                [8, 1, 2, 6, 4, 3, 9, 7, 5],
                [6, 5, 7, 8, 2, 9, 4, 1, 3],
                [1, 6, 3, 7, 9, 5, 8, 2, 4],
                [4, 2, 9, 3, 6, 8, 7, 5, 1],
                [5, 7, 8, 2, 1, 4, 6, 3, 9],
                [7, 4, 5, 9, 3, 6, 1, 8, 2],
                [2, 9, 6, 5, 8, 1, 3, 4, 7],
                [3, 8, 1, 4, 7, 2, 5, 9, 6]
            ]
        )
        # sanity check that I transfered the solution correctly
        solved = Sudoku(solution)
        self.assertTrue(solved.is_solved())

        # check that the solution is correct
        self.assertTrue( (s.grid == solution).all() )


if __name__ == "__main__":
    unittest.main()
