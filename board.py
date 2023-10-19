from const import *
from pieces import *

import pygame


class Board:
    def __init__(self):
        # Create window and title
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        # Text Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

        # Initial setup of the chessboard with pieces in their starting positions.
        # Game board stored as an array of piece objects
        self.game_state = [
            # Row 8
            [
                # Columns A-H
                Rook("black"),
                Knight("black"),
                Bishop("black"),
                Queen("black"),
                King("black"),
                Bishop("black"),
                Knight("black"),
                Rook("black"),
            ],
            # Row 7
            [Pawn("black") for _ in range(8)],
            # Rows 6 - 3
            # Colums A-H
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            # Row 2
            [Pawn("white") for _ in range(8)],
            # Row 1
            [
                # Columns A-H
                Rook("white"),
                Knight("white"),
                Bishop("white"),
                Queen("white"),
                King("white"),
                Bishop("white"),
                Knight("white"),
                Rook("white"),
            ],
        ]

        self.last_move = None

    def is_in_check(self, color):
        king_position = self.get_king_position(color)
        for y, row in enumerate(self.game_state):
            for x, piece in enumerate(row):
                if piece and piece.color != color:
                    if king_position in piece.possible_moves((x, y), self):
                        return True
        return False

    def get_king_position(self, color):
        for y, row in enumerate(self.game_state):
            for x, piece in enumerate(row):
                if isinstance(piece, King) and piece.color == color:
                    return (x, y)

    # Draw Moves
    # Draws all the possible moves for a piece
    def draw_moves(self, moves):
        for move in moves:
            pygame.draw.circle(self.window, GREY, ((BOARD_OFFSET + move[0] * SQSIZE) + SQSIZE // 2, (BOARD_OFFSET + move[1] * SQSIZE) + SQSIZE // 2), SQSIZE // 5)
            
    # Draws the row numbers on the board
    # Gets correct color and then draws on board
    def draw_row_numbers(self):
        for r in range(ROWS):
            color = LIGHT_SQAURE_COLOR if (r + 1) % 2 == 0 else DARK_SQUARE_COLOR 
            text = self.font.render(str(ROWS - r), 1, color)    
            self.window.blit(text, (BOARD_OFFSET + 10, BOARD_OFFSET + 10 + r * SQSIZE))

    # Draws the column letters on the board
    # Gets correct color and then draws on board
    def draw_column_letters(self):
        for c in range(COLS):
            color = DARK_SQUARE_COLOR if (c + 1) % 2 == 0 else LIGHT_SQAURE_COLOR
            text = self.font.render(chr(c + 97), 1, color)
            self.window.blit(text, ((BOARD_OFFSET + SQSIZE - 20) + c * SQSIZE, HEIGHT - BOARD_OFFSET - 25))

    # Draw the pieces on the board
    # Loops through the board array, and loads pieces onto the screen
    def draw_pieces(self):
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.game_state[r][c]
                if piece:
                    self.window.blit(piece.img, (BOARD_OFFSET + c * SQSIZE, BOARD_OFFSET + r * SQSIZE))
    
    # Drawing board 
    # Loops to get correct square color and then draws square
    def draw_board(self):
        self.window.fill(GREY)
        for r in range(ROWS):
            for c in range(COLS):
                # Deciding correct sqaure color
                color = LIGHT_SQAURE_COLOR if (r + c) % 2 == 0 else DARK_SQUARE_COLOR
                pygame.draw.rect(self.window, color, (BOARD_OFFSET + c * SQSIZE, BOARD_OFFSET + r * SQSIZE, SQSIZE, SQSIZE))
            
                if r == ROWS - 1:
                    self.draw_column_letters()

        self.draw_row_numbers()
        self.draw_pieces()
