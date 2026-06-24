# Timeline

I have "currated" my work as a commit-by-commit history, the .git dir is included.

# Solver design

- Started with a simple solver, which apparently was able to solve inputs 0-2:
```pseudocode
while not solved:
	propagate constraints
	fill any cells with only 1 candidate
	if none such cell exists fail, otherwise repeat
```

- Then noticed that input-3 was "invalid", as the first row/column/box duplicate the number 3

- For the shake of completeness I then added a "difficult" Sudoku, 
  that requires making a guess and backtracking if that guess leads to a "dead-end":
  a not-filled cell with no candidates left
  
# Limitations

Did not consider performance, e.g. python ~set~s could be replaced by bitmaps.
