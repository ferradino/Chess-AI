import sys
import pygame

pygame.init()

import engine
from display import *
from pieces import *
from const import FPS, SQSIZE, BOARD_OFFSET


class Main:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_state = engine.GameState()

        self.selected_square = ()
        self.clicked_squares = []
        self.move_made = False
        self.color_to_move = "white"  # mayne reomve this

    def game_loop(self):
        # Draw the board and the pieces on it
        draw_board(self.game_state.board)

        # Game Loop (runs until user clocks exit)
        while self.running:
            pygame.display.update()

            # Limits how fast the game loops (60fps)
            self.clock.tick(FPS)

            # Determine who's turn it is to move
            color_to_move = "white" if self.game_state.white_to_move else "black"

            if color_to_move == "black":
                # Event handling
                for event in pygame.event.get():
                    # If user clicked_square exit, exit program
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        position = (
                            (list(pygame.mouse.get_pos())[0] - BOARD_OFFSET)
                            // SQSIZE,  # (x, y) location of the mouse
                            (list(pygame.mouse.get_pos())[1] - BOARD_OFFSET) // SQSIZE,
                        )
                        col = position[0]
                        row = position[1]

                        # Check if click was out of bounds
                        if (row < 0 or row > 7) or (col < 0 or col > 7):
                            continue

                        # Clicked the same square twice
                        if (
                            self.selected_square == (row, col)
                            and len(self.clicked_squares) == 1
                        ):
                            self.square_selected = ()
                            self.clicked_squares = []

                        else:
                            # If not the same square, add it to the list
                            self.selected_square = (row, col)
                            self.clicked_squares.append(self.selected_square)

                        # Make sure first click is a white piece
                        game_object = self.game_state.board[row][col]
                        if len(self.clicked_squares) == 1:
                            # Clicked on a non white piece
                            if not game_object or game_object.color != color_to_move:
                                self.selected_square = ()
                                self.clicked_squares = []

                                draw_board(self.game_state.board)
                            # Clicked on a white piece
                            else:
                                moves = game_object.get_moves(
                                    (position),
                                    self.game_state.board,
                                    self.game_state.last_move,
                                )

                                draw_board(self.game_state.board)
                                draw_moves(moves)

                        elif len(self.clicked_squares) == 2:
                            # Make sure second square is a possible move
                            if position in moves:
                                move = engine.Move(
                                    self.clicked_squares[0],
                                    self.clicked_squares[1],
                                    self.game_state.board,
                                    self.game_state.last_move,
                                )
                                self.game_state.make_move(move)

                                draw_board(self.game_state.board)

                                self.move_made = True
                                self.square_selected = ()  # deselect square
                                self.clicked_squares = []  # reset list

                            # Clicked on another white piece, have to reset and redraw moves
                            elif game_object and game_object.color == color_to_move:
                                moves = game_object.get_moves(
                                    (position),
                                    self.game_state.board,
                                    self.game_state.last_move,
                                )

                                draw_board(self.game_state.board)
                                draw_moves(moves)

                                self.clicked_squares = [
                                    self.selected_square
                                ]  # setting list equal to current square selected

                            # Did not click on a possible move square or another white piece
                            else:
                                self.clicked_squares = [
                                    self.clicked_squares[0]
                                ]  # setting list equal to first square in list

                            if self.move_made == True:
                                if self.color_to_move == "white":
                                    self.color_to_move = "black"
                                else:
                                    self.color_to_move = "white"
            else:
                # Generate a move from the AI
                ai_move = self.game_state.ai_move()
                self.game_state.make_move(ai_move)

                draw_board(self.game_state.board)


if __name__ == "__main__":
    main = Main()
    main.game_loop()
