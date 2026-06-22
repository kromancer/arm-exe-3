#!/usr/bin/env python3
from argparse import ArgumentParser

import numpy as np
import yaml


class Sudoku(object):
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.validate_input_grid()

        self.row_candidates: list[set] = [ {x for x in range(1, 10)} for _ in range(9) ]
        self.col_candidates: list[set] = [ {x for x in range(1, 10)} for _ in range(9) ]

        # view boxes as a 3x3 grid
        self.box_candidates: list[list[set]] = [ [ {x for x in range(1, 10)} for _ in range(3) ] for _ in range(3) ]

        self.cell_candidates: list[list[set]] = [ [ set() for _ in range(9) ] for _ in range(9) ]

    def validate_input_grid(self) -> None:
        if self.grid.shape != (9, 9):
            raise ValueError("Input grid must be 9x9")

        if not (self.grid >= 0).all() or not (self.grid <= 9).all():
            raise ValueError("Input grid must contain only numbers 0-9")

        # no duplicates per box
        boxes = self.grid.reshape(3, 3, 3, 3).swapaxes(1, 2)
        for i in range(3):
            for j in range(3):
                box_no_zeroes = boxes[i, j, :, :][boxes[i, j, :, :] != 0]
                if len(box_no_zeroes) != len(set(box_no_zeroes)):
                    raise ValueError(f"Duplicate numbers in box {i, j}")

        # no duplicates per column
        for col in range(9):
            col_no_zeros = self.grid[:, col][self.grid[:, col] != 0]
            if len(col_no_zeros) != len(set(col_no_zeros)):
                raise ValueError(f"Duplicate numbers in column {col}")

        # no duplicates per row
        for row in range(9):
            row_no_zeros = self.grid[row, :][self.grid[row, :] != 0]
            if len(row_no_zeros) != len(set(row_no_zeros)):
                raise ValueError(f"Duplicate numbers in row {row}")

    def __str__(self) -> str:
        s = ""
        for row in range(9):
            if row % 3 == 0 and row != 0:
                s += "-----------------------\n"
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    s += " | "
                s += str(self.grid[row, col]) + " "
            s += "\n"
        return s

    def is_solved(self) -> bool:
        return self.check_rows() and self.check_cols() and self.check_boxes()

    def check_rows(self) -> bool:
        all_numbers = set(range(1, 10))
        for row in self.grid:
            if len(all_numbers - set(row)) != 0:
                return False
        return True

    def check_cols(self) -> bool:
        all_numbers = set(range(1, 10))
        for col in self.grid.T:
            if len(all_numbers - set(col)) != 0:
                return False
        return True

    def check_boxes(self) -> bool:
        all_numbers = set(range(1, 10))
        boxes = self.grid.reshape(3, 3, 3, 3).swapaxes(1, 2)
        for i in range(3):
            for j in range(3):
                if len(all_numbers - set(boxes[i, j, :, :].flatten())) != 0:
                    return False
        return True

    def _solve(self):
        while not self.is_solved():
            if not self.propagate_constraints():
                # not solvable grid
                return None

            if not self.assign():
                # there is no cell with a single assignment candidate,
                # we should make a guess
                min_row, min_col = self.find_cell_with_min_candidates()
                while len(self.cell_candidates[min_row][min_col]) > 0:
                    candidate = self.cell_candidates[min_row][min_col].pop()
                    new_grid = self.grid.copy()
                    new_grid[min_row, min_col] = candidate
                    solved_or_not = Sudoku(new_grid)._solve()
                    if solved_or_not is not None:
                        return solved_or_not
                return None

        return self


    def solve(self):
        solved = self._solve()
        if solved is not None:
            self.grid = solved.grid

    def propagate_constraints(self) -> bool:
        """
        Given a partially-filled grid:
        - update the row, column, and box candidates
        - each cell's candidates is then just the intersection of the corresponding row, column, and box candidates

        :return: True if every cell has at least one candidate, False otherwise
        """
        for row in range(9):
            self.row_candidates[row] -= set(self.grid[row, :]) - {0}
        for col in range(9):
            self.col_candidates[col] -= set(self.grid[:, col]) - {0}

        boxes = self.grid.reshape(3, 3, 3, 3).swapaxes(1, 2)
        for i in range(3):
            for j in range(3):
                self.box_candidates[i][j] -= set(boxes[i, j, :, :].flatten()) - {0}

        for row in range(9):
            for col in range(9):

                # do not touch cells that are already filled
                if self.grid[row, col] != 0:
                    assert len(self.cell_candidates[row][col]) == 0, "Invariant violated: filled cell has candidates!"
                    continue

                self.cell_candidates[row][col] = (self.row_candidates[row] &
                                                  self.col_candidates[col] &
                                                  self.box_candidates[row // 3][col // 3])

                if len(self.cell_candidates[row][col]) == 0 and self.grid[row, col] == 0:
                    # no candidates left for this cell, and it's not already filled!
                    return False

        return True

    def assign(self) -> bool:
        # find a cell with a single candidate, and assign it
        for row in range(9):
            for col in range(9):
                if len(self.cell_candidates[row][col]) == 1:
                    self.grid[row, col] = self.cell_candidates[row][col].pop()
                    return True
        return False

    def find_cell_with_min_candidates(self) -> tuple[int, int]:
        min_candidates = 9
        min_cell = None
        for row in range(9):
            for col in range(9):
                if 0 < len(self.cell_candidates[row][col]) <= min_candidates:
                    min_candidates = len(self.cell_candidates[row][col])
                    min_cell = (row, col)
        assert min_cell is not None
        return min_cell

def run_sudoku(grid: np.ndarray, is_verbose: bool) -> np.ndarray:
    sudoku = Sudoku(grid)

    if is_verbose:
        print(sudoku)

    sudoku.solve()

    if is_verbose:
        print(sudoku)

    return sudoku.grid

def compare(source, reference):
    for row in range(9):
        for col in range(9):
            if source[row][col] != reference[row][col]:
                return False
    
    return True

if __name__ == "__main__":
    parser = ArgumentParser(description="Solve Sudokus, store their solution and if a reference is provided, compare against it")
    parser.add_argument("test_spec", help="A yaml containing a list of dicts for the input/output/reference .npy files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print sudoku before/after solution")
    args = parser.parse_args()

    with open(args.test_spec) as f:
        test_spec = yaml.safe_load(f)

    for tc in test_spec:
        if args.verbose:
            print(f"Solving {tc['input']}")

        try:
            out = run_sudoku(np.load(tc["input"]), args.verbose)
            if "reference" in tc and not compare(out, np.load(tc["reference"])):
                print(f"Solution does not match reference for: {tc['input']}")
            np.save(tc["output"], out)
        except ValueError as e:
            print(f"Input grid validation failed for: {tc['input']}")
            print(e)
