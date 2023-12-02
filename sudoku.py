import pygame
from constants import *
from board import Board
from cell import Cell

def main():

    # Start by creating the pygame window
    pygame.init()
    pygame.display.set_caption("Sudoku Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Use a clock to set the game to a fixed framerate
    fps_clock = pygame.time.Clock()

    # Initialize the fonts
    big_font = pygame.font.Font("arial_bold.ttf", 65)
    button_font = pygame.font.Font("arial.ttf", 25)
    Cell.font_big = pygame.font.Font("arial_bold.ttf", 50)
    Cell.font_small = pygame.font.Font("arial_bold.ttf", 25)

    # This variable keeps track of which state the game is in
    # This controls what is drawn and which events are active
    state = 'main_menu'

    # Keep running the program
    is_running = True
    while is_running:

        # Keeps track of which key & mouse events occured
        num_press = None
        mouse_press = None
        enter_press = False
        backspace_press = False
        arrow_press = None

        # Check for events
        for event in pygame.event.get():

            # Perform action if left clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_press = event.pos

            # Perform action if key was pressed
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN):
                    enter_press = True
                elif (event.key == pygame.K_BACKSPACE):
                    backspace_press = True
                elif (event.unicode and event.unicode in '123456789'):
                    num_press = int(event.unicode)
                elif (event.key == pygame.K_UP):
                    arrow_press = 'up'
                elif (event.key == pygame.K_DOWN):
                    arrow_press = 'down'
                elif (event.key == pygame.K_LEFT):
                    arrow_press = 'left'
                elif (event.key == pygame.K_RIGHT):
                    arrow_press = 'right'

            # Stop program if the window is closed
            if event.type == pygame.QUIT:
                is_running = False

        # Refresh with a white background
        screen.fill(C_WHITE)

        # If on the main menu...
        if (state == 'main_menu'):

            # Draw the top text
            text_surf = big_font.render("Sudoku!", True, C_BLACK)
            screen.blit(text_surf, (WIDTH/2 - text_surf.get_width()/2, 150))
            text_surf = button_font.render("Select a difficulty:", True, C_BLACK)
            screen.blit(text_surf, (WIDTH/2 - text_surf.get_width()/2, 300))
            
            # Draw the buttons for difficulty
            draw_button((WIDTH/2 - 150, 400), (120, 40), "Easy", C_GREEN, button_font, screen)
            draw_button((WIDTH/2, 400), (120, 40), "Medium", C_YELLOW, button_font, screen)
            draw_button((WIDTH/2 + 150, 400), (120, 40), "Hard", C_RED, button_font, screen)

            # If clicked on a button, create a board
            if (mouse_press is not None):
                for i in range(3):
                    if (is_inside_button(*mouse_press, (WIDTH/2 + 150 * (i - 1), 400), (120, 40))):
                        difficulty = ["easy", "medium", "hard"][i]
                        board = Board(9, 9, screen, difficulty)
                        state = 'game'

        # If playing the game...
        elif (state == 'game'):

            # Select new cell
            if (mouse_press is not None):
                clicked_cell = board.click(*mouse_press)
                if (clicked_cell is not None):
                    board.select(clicked_cell[0],clicked_cell[1])

            # Sketch the number
            if (num_press is not None):
                board.sketch(num_press)

            # Set the number
            if (enter_press):
                board.place_number()

            # Erase the number
            if (backspace_press):
                board.clear()

            # Arrow keys move between cells
            if (arrow_press is not None):
                board.move_position(arrow_press)

            # Draw the sudoku board and the buttons under it
            board.draw()
            draw_button((WIDTH/2 - 120, 570), (100, 40), "Reset",C_YELLOW,button_font,screen)
            draw_button((WIDTH/2, 570), (100, 40), "Restart",C_YELLOW,button_font,screen)
            draw_button((WIDTH/2 + 120, 570), (100, 40), "Exit",C_YELLOW,button_font,screen)

            # Check if any buttons were clicked
            if (mouse_press is not None):
                # reset
                if is_inside_button(*mouse_press, (WIDTH/2 - 120, 570), (100, 40)):
                    board.reset_to_original()
                # restart
                elif is_inside_button(*mouse_press, (WIDTH/2, 570), (100, 40)):
                    state = 'main_menu'
                # exit
                elif is_inside_button(*mouse_press, (WIDTH/2 + 120, 570), (100, 40)):
                    is_running = False

        # If on the win screen...
        elif (state == 'win'):

            # Draw the top text
            text_surf = big_font.render("You won!", True, C_BLACK)
            screen.blit(text_surf, (WIDTH/2 - text_surf.get_width()/2, 150))
            
            # Draw the exit button
            draw_button((WIDTH/2, 400), (120, 40), "Exit", C_GREEN, button_font, screen)

            # Quit if exit was pressed
            if (mouse_press is not None):
                if (is_inside_button(*mouse_press, (WIDTH/2, 400), (120, 40))):
                    is_running = False

        # If on the lose screen...
        elif (state == 'lose'):

            # Draw the top text
            text_surf = big_font.render("You lost :(", True, C_BLACK)
            screen.blit(text_surf, (WIDTH/2 - text_surf.get_width()/2, 150))
            
            # Draw the restart button
            draw_button((WIDTH/2, 400), (120, 40), "Restart", C_GREEN, button_font, screen)

            # Start a new game if restart was pressed
            if (mouse_press is not None):
                if (is_inside_button(*mouse_press, (WIDTH/2, 400), (120, 40))):
                    state = 'main_menu'

        # Wait 1/30th of a frame
        pygame.display.update()
        fps_clock.tick(30)

# Draws a button to the screen
def draw_button(center, size, text, color, font, screen):
    text_surf = font.render(text, True, C_BLACK)
    pygame.draw.rect(screen, color, (center[0] - size[0]/2, center[1] - size[1]/2, *size))
    screen.blit(text_surf, (center[0] - text_surf.get_width()/2, center[1] - text_surf.get_height()/2))

# Returns whether a button was clicked
def is_inside_button(x, y, center, size):
    return (center[0] - size[0]/2 <= x <= center[0] + size[0]/2) and (center[1] - size[1]/2 <= y <= center[1] + size[1]/2)

if __name__ == '__main__':
    main()