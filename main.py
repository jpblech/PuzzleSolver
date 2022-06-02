
# puzzle_piece is an list of each piece we may use, each element contains an three elements, 1st is the id number
# assigned to that piece, 2nd if the piece has been rotated, 0  original position 1 for rotated, 3rd element is a
# binary presentation of the piece
puzzle_pieces = [[1, 0, [[1, 0, 0, 0, 0], [0, 0, 1, 0, 1]]], [2, 0, [[1, 0, 0, 1, 0], [0, 0, 0, 0, 1]]],
                 [3, 0, [[1, 0, 1, 0, 0], [0, 1, 0, 0, 0]]], [4, 0, [[0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]],
                 [5, 0, [[0, 1, 0, 1, 0], [0, 1, 0, 0, 0]]], [6, 0, [[0, 0, 0, 0, 1], [0, 1, 0, 1, 0]]],
                 [7, 0, [[0, 0, 0, 0, 1], [1, 1, 0, 0, 0]]], [8, 0, [[1, 0, 0, 0, 1], [0, 0, 0, 0, 1]]]]

# State tracks the position of the current puzzle pieces in the puzzle we use list of list to represent 5*5 matrix
state = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

# order tracks what piece have been added to our puzzle
order = []


def solve_puzzle():
    place = 0
    search(state, puzzle_pieces, place)
    return state


def piece_fits(state, piece, position):
    # Checks if the current piece can fit in the state and position
    #
    # @param state = the current state of piece already in board
    # @param piece = current piece we would like to try
    # @param position = the current position we are trying
    # @return Boolean
    for _ in order:
        if piece in order:
            return False
    if (position % 4 == 1) & (piece[2][1][2] == 1):
        return False
    if (position % 4 == 2) & (piece[2][0][2] == 1):
        return False
    for i in range(5):
        if state[position % 4][i] & int(piece[2][0][i]):
            return False
    for i in range(5):
        if state[(position % 4) + 1][i] & int(piece[2][1][i]):
            return False
    return True


def add_piece(piece, position, state):
    # Adds piece to the puzzle need to check first if puzzle piece fits
    #
    # @param state = the current state of piece already in board
    # @param piece = current piece we would like to add
    # @param position = the current position we are trying
    # @return the state with piece added

    # current position we are trying to add
    x = position % 4
    # add piece to order
    order.append(piece)
    for i in range(5):
        state[x][i] = state[x][i] | piece[2][0][i]
    for i in range(5):
        state[x + 1][i] = state[x + 1][i] | piece[2][1][i]
    return state


def backwards(piece):
    # Rotates piece 180 deg
    #
    # @param piece = piece to rotate
    # @returns rotated piece
    for j in range(5):
        buff = piece[2][0][j]
        piece[2][0][j] = piece[2][1][4 - j]
        piece[2][1][4 - j] = buff
    return piece[2]


def rotate(piece, side):
    # Checks if piece needs to be rotated
    # @param piece = piece to rotate
    # @param side = binary number denoting if we want to rotate or not
    # @return piece in the correct angle
    for a in order:
        if a[0] == piece[0]:
            return piece[2]
    if side == 0:
        return piece[2]
    else:
        piece[1] = piece[1] ^ 1
        return backwards(piece)


def rotate_board(state):
    # Rotates the board, use linear algebra idea of transpose and returns a transpose matrix of the current board
    #
    # @param state = current state of board
    # @returns transposed matrix
    return [[state[j][i] for j in range(len(state))] for i in range(len(state[0]))]


def remove_from_board(state):
    # Removes last piece that was added to the puzzle
    #
    # @param state = current state of board
    # @returns puzzle with out the last piece added

    x = (len(order) - 1) % 4

    # Removes last piece from the order list
    piece = order.pop()
    for i in range(5):
        if piece[2][0][i] == 1:
            state[x][i] = 0
    for i in range(5):
        if piece[2][1][i] == 1:
            state[x + 1][i] = 0
    if piece[1] == 1:
        piece[2] = rotate(piece, 1)
    return state


def search(state, puzzle_pieces, place):
    # This function uses recursion/backtracking in order to try all the possible combinations
    # and returns the true once found
    #
    # @param state = current state of puzzle
    # @param puzzle_piece = list of puzzle pieces
    # @param place = current position we are trying to solve
    # @return boolean if the puzzle search was successful

    # Runs the possible positions
    for position in range(8):
        # checks that position is in the same position as place
        if position == place:
            # If we have added 4 pieces to our puzzle we rotate it
            if position == 4:
                state = rotate_board(state)
            # Iterate through puzzle pieces
            for piece in puzzle_pieces:
                # Tries both angle of the current piece
                for side in range(2):
                    piece[2] = rotate(piece, side)
                    # Checks if piece fits in our current puzzle if so adds piece
                    if piece_fits(state, piece, position):
                        state = add_piece(piece, position, state)
                        place += 1
                        # Recursion caller if return try if we fit all the pieces
                        if search(state, puzzle_pieces, place):
                            return True
                        # If false removes last piece and tries rest of the pieces in current position
                        else:
                            if position == 4:
                                state = rotate_board(state)
                            state = remove_from_board(state)
                            place -= 1
                    # If piece has been rotated return it to original position
                    elif piece[1] == 1:
                        piece[2] = rotate(piece, 1)
        else:
            continue
        return False
    return True


def print_puzzle(order):
    # Print solved puzzle
    #
    # @param order = list of pieces of solved puzzle
    # print puzzle
    for i in range(11):
        for x in range(11):
            if i == 0 or i == 10:
                if x > 0 and x % 2 == 0 and x < 10 and i != 10:
                    print("V", end="")
                    print(order[x//2 - 1][0], end="")
                else:
                    print("  ", end="")
            else:
                if i % 2 == 0:
                    if x % 2 == 0 and x != 0 and x != 10:
                        print("||", end="")
                    elif x != 0 and x != 10:
                        print("==", end="")
                    elif x == 0:
                        print(order[i//2 + 3][0], end="")
                        print(">", end="")
                    else:
                        print("  ", end="")
                else:
                    if x % 2 == 0 and x != 0 and x != 10:
                        print("||", end="")
                    else:
                        print("  ", end="")
        print("")


def print_puzzle_text(order):
    # Print out a text explanation of how to assemble the puzzle
    #
    # @param order = the order the puzzle was assembled

    print("Puzzle pieces are numbered 1-8 according to the picture from right to left.")
    print("We assemble the first 4 puzzle piece in order of"
        " left to right where they are vertical with back facing up.\n")
    for idx, piece in enumerate(order):
        if idx < 4:
            if piece[1] == 1:
                print("We place piece {} rotated 180".format(piece[0]))
            else:
                print("We place piece {} in original direction".format(piece[0]))
        else:
            if idx == 4:
                print(
                    "\n We then assemble the next 4 puzzle piece in order of up to down where rotate them "
                    "90 degree until clockwise  with back facing down.\n")
            if piece[1] == 1:
                print("We place piece {} rotated 180".format(piece[0]))
            else:
                print("We place piece {} in original direction".format(piece[0]))


if __name__ == '__main__':
    # Find solution to puzzle return puzzle solved with print out of puzzle if not
    # possible print to screen not solvable
    if solve_puzzle():
        print("Puzzle Solved!!")
        print_puzzle(order)
        print_puzzle_text(order)
    else:
        print("Puzzle not solvable")
