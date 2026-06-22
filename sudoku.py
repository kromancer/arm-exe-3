#!/usr/bin/env python3
from argparse import ArgumentParser

import numpy as np
import yaml


class Sudoku(object):
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.row_candidates: list[set] = [ {x for x in range(1, 10)} for _ in range(9) ]
        self.col_candidates: list[set] = [ {x for x in range(1, 10)} for _ in range(9) ]

        # view boxes as a 3x3 grid
        self.box_candidates: list[list[set]] = [ [ {x for x in range(1, 10)} for _ in range(3) ] for _ in range(3) ]

        self.cell_candidates: list[list[set]] = [ [ set() for _ in range(9) ] for _ in range(9) ]

    def __str__(self):
        pass

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

    def solve(self):
        while not self.is_solved():
            self.propagate_constraints()

            if not self.assign():
                print("No position with a single candidate, giving-up")
                break

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

def run_sudoku(grid: np.ndarray) -> np.ndarray:
    sudoku = Sudoku(grid)
    sudoku.solve()
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
    args = parser.parse_args()

    with open(args.test_spec) as f:
        test_spec = yaml.safe_load(f)

    for tc in test_spec:
        out = run_sudoku(np.load(tc["input"]))

        if "reference" in tc and not compare(out, np.load(tc["reference"])):
            print(f"Solution does not match reference for: {tc['input']}")

        np.save(tc["output"], out)

