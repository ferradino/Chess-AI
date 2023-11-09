from const import *
import pygame


# Create window and title
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Text Font
font = pygame.font.Font(pygame.font.get_default_font(), 20)

# Draw Moves
# Draws all the possible moves for a piece
def draw_moves(moves):
    for move in moves:
        pygame.draw.circle(window, GREY, ((BOARD_OFFSET + move[0] * SQSIZE) + SQSIZE // 2, (BOARD_OFFSET + move[1] * SQSIZE) + SQSIZE // 2), SQSIZE // 5)

# Draws the row numbers on the board
# Gets correct color and then draws on board
def draw_row_numbers():
    for r in range(ROWS):
        color = LIGHT_SQAURE_COLOR if (r + 1) % 2 == 0 else DARK_SQUARE_COLOR 
        text = font.render(str(ROWS - r), 1, color)    
        window.blit(text, (BOARD_OFFSET + 10, BOARD_OFFSET + 10 + r * SQSIZE))

# Draws the column letters on the board
# Gets correct color and then draws on board
def draw_column_letters():
    for c in range(COLS):
        color = DARK_SQUARE_COLOR if (c + 1) % 2 == 0 else LIGHT_SQAURE_COLOR
        text = font.render(chr(c + 97), 1, color)
        window.blit(text, ((BOARD_OFFSET + SQSIZE - 20) + c * SQSIZE, HEIGHT - BOARD_OFFSET - 25))

# Draw the pieces on the board
# Loops through the board array, and loads pieces onto the screen
def draw_pieces(board):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece:
                window.blit(piece.img, (BOARD_OFFSET + c * SQSIZE, BOARD_OFFSET + r * SQSIZE))

# Drawing board 
# Loops to get correct square color and then draws square
def draw_board(board):
    window.fill(GREY)
    for r in range(ROWS):
        for c in range(COLS):
            # Deciding correct sqaure color
            color = LIGHT_SQAURE_COLOR if (r + c) % 2 == 0 else DARK_SQUARE_COLOR
            pygame.draw.rect(window, color, (BOARD_OFFSET + c * SQSIZE, BOARD_OFFSET + r * SQSIZE, SQSIZE, SQSIZE))

            if r == ROWS - 1:
                draw_column_letters()

    draw_row_numbers()
    draw_pieces(board)

