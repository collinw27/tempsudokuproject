import pygame
from constants import *
from cell import Cell
from sudoku_generator import generate_sudoku

class Board:

    # Initialize with width, pygame screen, and difficulty
    # The cell values are sourced from a SudokuGenerator instance
    def __init__(self, width, height, screen, difficulty):

        self.width = width
        self.height = height
        self.screen = screen
        self.position = None

        # Generate a board with the given size & difficulty parameters
        num_empty = {'easy': 30, 'medium': 40, 'hard': 50}
        board = generate_sudoku(max(width, height), num_empty[difficulty])

        # Then, convert each number in the board to a Cell instance
        self.board = [ [ Cell(cell, x, y, screen) for x, cell in enumerate(row) ] for y, row in enumerate(board) ]

    def draw(self):

        # Each cell covers a 60x60 area
        # Start by drawing horizontal lines 60px apart
        # Every third line is bolded
        for i in range(10):
            x = i * 60
            pygame.draw.line(self.screen, C_BLACK, (x, 0), (x, 540), width = (3 if i % 3 == 0 else 1))
        # Now, do the same thing for vertical lines
        for i in range(10):
            y = i * 60
            pygame.draw.line(self.screen, C_BLACK, (0, y), (540, y), width = (3 if i % 3 == 0 else 1))

        # Draw every cell
        for row in self.board:
            for cell in row:
                cell.draw()

        # Draw a red square around the selected cell
        if (self.position is not None):
            pygame.draw.rect(self.screen, C_RED, (self.position[1] * 60, self.position[0] * 60, 60, 60), width = 3)

    def select(self, row, col):
        self.position = [row,col]

    def click(self, x, y):
        row = y//60
        col = x//60
        #checks if in range of board
        if (0 <= row <= 8 and 0 <= col <=8):
            return (row, col)
        else:
            return None

    # resets the sketch & real value of the selected cell
    def clear(self):
        if (self.position is not None):
            cell = self.board[self.position[0]][self.position[1]]
            cell.set_cell_value(0)
            cell.set_cell_sketch_value(0)

    # sets the sketch value of the selected cell
    def sketch(self, value):
        if (self.position is not None):
            cell = self.board[self.position[0]][self.position[1]]
            cell.set_cell_value(0)
            cell.set_cell_sketch_value(value)

    # copies the cell's value from its sketch value
    def place_number(self):
        if (self.position is not None):
            cell = self.board[self.position[0]][self.position[1]]
            cell.set_cell_to_sketch()

    def reset_to_original(self):
        # iterate over every cell and reset its value
        for i in range(0,9):
            for j in range(0,9):
                self.board[i][j].set_cell_value(0)

    def is_full(self):
        # cells are empty if their value is 0
        # if any cell's value is 0, is_full returns false
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j].value != 0:
                    continue
                else:
                    return False
        return True

    def find_empty(self):
        pass

    def check_board(self):
        pass

    def move_position(self, direction):
        # Don't do anything if deselected
        if (self.position is None):
            return
        # Move in the specified direction otherwise
        # Uses min() and max() to stay within the bounds
        if (direction == 'up'):
            self.position[0] = max(self.position[0] - 1, 0)
        elif (direction == 'down'):
            self.position[0] = min(self.position[0] + 1, 8)
        elif (direction == 'left'):
            self.position[1] = max(self.position[1] - 1, 0)
        elif (direction == 'right'):
            self.position[1] = min(self.position[1] + 1, 8)