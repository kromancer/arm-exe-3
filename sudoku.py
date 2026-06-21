#!/usr/bin/env python3
from argparse import ArgumentParser

import numpy as np
import yaml


class Sudoku(object):
    def __init__(self, grid: np.ndarray):
        self.grid = grid

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
        pass

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

