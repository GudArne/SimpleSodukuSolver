import pygame
import sys
import random

from main import is_safe, print_board, solve_sudoku

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.SysFont("Arial", 40)

def draw_grid(screen):
    for i in range(1, GRID_SIZE):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thickness)

def draw_numbers(screen, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 10))

def draw_selection(screen, row, col):
    pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def generate_sudoku():
    base = 3
    side = base * base

    while True:
        nums = random.sample(range(1, side + 1), side)
        board = [[0] * side for _ in range(side)]

        for p in range(side):
            for q in range(side):
                num = nums[(p * base + q) % side]
                row, col = p, q

                attempts = 0
                max_attempts = 10

                while not is_safe(board, row, col, num):
                    random.shuffle(nums)
                    num = nums[(p * base + q) % side]
                    attempts += 1

                    if attempts >= max_attempts:
                        attempts = 0
                        random.shuffle(nums)
                        board = [[0] * side for _ in range(side)]
                        break

                if attempts >= max_attempts:
                    break

                board[row][col] = num

        if attempts < max_attempts:
            break  # A valid board was generated, exit the loop

    # Continue with the shuffling and emptying cells as before
    all_cells = [(i, j) for i in range(side) for j in range(side)]
    random.shuffle(all_cells)

    empty_cells = 40
    for _ in range(empty_cells):
        row, col = all_cells.pop()
        board[row][col] = 0

    return board



def main():
    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Solver")

    # Generate a Sudoku puzzle
    sudoku_board = generate_sudoku()

    # Variables for user input
    selected = None
    key_input = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                selected = (row, col)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isnumeric():
                    key_input = int(event.unicode)
                elif event.key == pygame.K_RETURN:
                    # Solve the puzzle when the Enter key is pressed
                    if solve_sudoku(sudoku_board):
                        print("\nSudoku solution:")
                        print_board(sudoku_board)
                    else:
                        print("\nNo solution exists.")
                elif event.key == pygame.K_r:
                    # Reset the puzzle when the R key is pressed
                    sudoku_board = generate_sudoku()

        screen.fill(WHITE)

        # Draw the Sudoku grid
        draw_grid(screen)

        # Draw numbers on the board
        draw_numbers(screen, sudoku_board)

        # Highlight the selected cell
        if selected:
            draw_selection(screen, *selected)

        # Draw user input
        if selected and key_input is not None:
            sudoku_board[selected[0]][selected[1]] = key_input
            key_input = None

        pygame.display.flip()

if __name__ == "__main__":
    main()
