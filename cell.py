from constants import *

class Cell:

    # All cell instances store a reference to the same font instance
    font_big = None
    font_small = None

    def __init__(self, value, row, col, screen):
        self.value = value
        self.user_filled_in = (value == 0)
        self.sketch_value = 0
        self.row = row
        self.col = col
        self.screen = screen

    # if not filled in by default, set the cell's value
    def set_cell_value(self, value):
        if self.user_filled_in:
            self.value = value

    # if not filled in by default, set the cell's sketch value
    def set_cell_sketch_value(self, sketch_value):
        if self.user_filled_in:
            self.sketch_value = sketch_value

    # copy the cells value from its sketch value
    def set_cell_to_sketch(self):
        if (self.user_filled_in and self.sketch_value != 0):
            self.value = self.sketch_value
            self.sketch_value = 0

    def draw(self):

        # If its regular value is not 0, draw it at the correct position
        if (self.value != 0):
            text_surf = self.font_big.render(str(self.value), True, C_BLACK)
            self.screen.blit(text_surf, (self.row * 60 + 15, self.col * 60 + 10))

        # Otherwise, draw a sketch value if it exists
        elif (self.sketch_value != 0):
            text_surf = self.font_small.render(str(self.sketch_value), True, C_GRAY)
            self.screen.blit(text_surf, (self.row * 60 + 5, self.col * 60 + 5))