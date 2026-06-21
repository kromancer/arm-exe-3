#!/usr/bin/env python3
from argparse import ArgumentParser

import numpy as np
import yaml


class Sudoku(object):
    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def __str__(self):
        pass

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

