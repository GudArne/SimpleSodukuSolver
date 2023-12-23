def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()


def is_safe(board, row, col, num):
    # Check if 'num' is not present in the current row, column, and 3x3 box
    return (
        not used_in_row(board, row, num)
        and not used_in_col(board, col, num)
        and not used_in_box(board, row - row % 3, col - col % 3, num)
    )


def used_in_row(board, row, num):
    return num in board[row]


def used_in_col(board, col, num):
    return num in [board[i][col] for i in range(9)]


def used_in_box(board, start_row, start_col, num):
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return True
    return False


def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1


def solve_sudoku(board):
    row, col = find_empty_location(board)

    # If there is no empty location, the puzzle is solved
    if row == -1 and col == -1:
        return True

    # Try placing a number from 1 to 9
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            # Place the number if its safe
            board[row][col] = num

            # Recursively solve the rest of the puzzle
            if solve_sudoku(board):
                return True

            # If placing the current number doesnt lead to a solution, backtrack
            board[row][col] = 0

    # No solution found for the current configuration
    return False


if __name__ == "__main__":
    # Example board. 0 represents empty cells
    sudoku_board = [
        [8, 0, 7, 0, 1, 0, 5, 0, 0],
        [0, 5, 0, 3, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 7],
        [0, 8, 0, 4, 0, 0, 0, 5, 0],
        [0, 9, 5, 0, 0, 0, 4, 2, 0],
        [0, 3, 0, 0, 0, 9, 0, 7, 0],
        [6, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 1, 0, 6, 0],
        [0, 0, 9, 0, 8, 0, 1, 0, 5],
    ]

    print("Sudoku puzzle:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\nSudoku solution:")
        print_board(sudoku_board)
    else:
        print("\nNo solution exists.")
