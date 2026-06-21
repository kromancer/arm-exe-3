#!/usr/bin/env python3

class Sudoku(object):
    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        pass

    def solve(self):
        pass

def run_sudoku(input):
    sudoku = Sudoku(input)
    sudoku.solve()
    print(sudoku)
    
    return sudoku.grid

def compare(source, reference):
    for row in range(9):
        for col in range(9):
            if source[row][col] != reference[row][col]:
                return False
    
    return True

