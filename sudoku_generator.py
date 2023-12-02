import random

class SudokuGenerator:

    def __init__(self, row_length=9, removed_cells=0):
        # initializes box length (3), row length (9), # of removed cells, and the blank board
        self.box_length = 3
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for slot in range(self.row_length)] for slot in range(self.row_length)]

    def get_board(self):
        # returns the board, which was previously initialized in beginning or altered by following methods
        return self.board

    def valid_in_row(self, row, num):
        # checks if number is already present in row
        if num not in self.board[row]:
            return True
        else:
            return False

    def valid_in_col(self, col, num):
        # checks if number is already in column
        for row in range(0, self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        # checks if number is already in the 3x3 box
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        # uses previous three methods to determine if a number placement is valid or not
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        # integer division will identify the index of the box we are in (0, 1, 2). Multiplying this by 3 will give the start
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        if not self.valid_in_box(box_row_start, box_col_start, num):
            return False

        return True

    def fill_box(self, row_start, col_start):
        # fills a box with random valid integers
        # using a set means that valid_in_box is redundant
        unused_in_box = set(range(1,10))

        # goes through each of the 9 boxes left to right, top to bottom
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                # randomly selects a number from within the box
                number = random.choice(list(unused_in_box))
                self.board[row][col] = number
                # removes a number after it is used to ensure every number is valid in box
                unused_in_box.remove(number)

    # fills three boxes; top left, middle, and bottom right
    def fill_diagonal(self):
        for pos in range(0, self.row_length, 3):
            # diagonal boxes will have the same horizontal and vertical position
            self.fill_box(pos, pos)

    # fills remaining boxes
    # code is copied verbatim from Zhou (2022)
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        # if statements ensure numbers are valid
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        # if statements ensure numbers are valid
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        # uses validity methods to ensure added numbers are valid
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    # fills values into every slt of sudoku board
    # code copied directly from Zhou (2022)
    def fill_values(self):
        # first calls fill_diagonal method to fill three diagonal boxes
        self.fill_diagonal()
        # then calls fill_remaining method to fill remaining boxes
        self.fill_remaining(0, self.box_length)

    # removes cells according to initialized value
    def remove_cells(self):
        # cells to remove is specified by game difficulty; easy = 30, medium = 40, hard = 50
        cells_to_remove = self.removed_cells

        # randomly removes correct number of cells / creates correct number of empty cells
        while cells_to_remove > 0:
            # uses self.row_length because index of 8 will correspond to slot 9 (row length)
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            # checks if a slot has already been emptied before clearing it
            if self.board[row][col] != 0:
                # if slot is not already empty, that slot is cleared
                self.board[row][col] = 0
                # when slot is emptied, the remaining number of slots to clear goes down by one
                cells_to_remove -= 1

    # static method to generate sudoku board and use methods
    # code copied directly from Zhou (2022)

    def print_board(self):
        for row in self.board:
            row_str = ""
            for num in row:
                if num != 0:
                    row_str += str(num) + " "
                else:
                    row_str += "0 "
            print(row_str)


def generate_sudoku(size, removed):
    # step 1, creates blank board, but function call specifies the number of removed cells (difficulty)
    sudoku = SudokuGenerator(size, removed)
    # step 2, completely fills board with random but valid integers 1-9
    sudoku.fill_values()
    board = sudoku.get_board()
    # step 3, removes the number of cells determined by difficulty. Again, easy = 30, medium = 40, hard = 50
    sudoku.remove_cells()
    board = sudoku.get_board()
    # returns final board
    return board

# Code cited:
''' Zhou, L. 2022. Sudoku-Project, sudoku_generator.py [python]. Github.com.https://github.com/zhoulisha/Sudoku-Proj
        ect/blob/main/sudoku_generator.py'''
