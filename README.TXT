The program solve a Parquet wood puzzle, it uses backtracking/recursion
inorder to try every combination to find the correct assembly. Once found
the program will print out a small diagram and then explain exactly how to
assemble correctly.

The board is represented in a list as a 5*5 matrix using binary to mark if the current
block has been filled or not. Each piece is represented as 2*5 matrix in the same way.

The program will try each piece horizontally from up to down, if a piece does not fit it
will then rotate it 180 to try the second direction. Once the program has place 4 pieces it
will then transpose the matrix and try the remanding piece in the same way