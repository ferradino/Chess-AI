import sys
import pygame

from board import Board
from pieces import *
from const import FPS, SQSIZE, BOARD_OFFSET

class Main():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.board = Board()

    def game_loop(self):
        # Draw the board and the pieces on it
        self.board.draw_board()
        running = True
        selected = False

        # Game Loop (runs until user clocks exit)
        while running:
            # Limits how fast the game loops (60fps)
            self.clock.tick(FPS)
        
            # Event handling
            for event in pygame.event.get():
                # If user clicks exit, exit program
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()


                """ TODO """
                # Restructure the code below to:
                # 
                # Get mouse position
                # And object at that position
                #
                # If not selected and white
                #   get moves 
                #   draw moves
                #   select is true
                #
                # If selected and white
                #   get moves
                #   draw moves
                #
                # If selected and black
                #   set white piece to new pos
                #   update old pos to none
                #   redraw board
                #   seletect is false


                # Get position of mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected == False:
                        start_pos = ((list(pygame.mouse.get_pos())[0] - BOARD_OFFSET) // SQSIZE, # xpos
                                     (list(pygame.mouse.get_pos())[1] - BOARD_OFFSET) // SQSIZE) # ypos
                        
                        # Get object at that position
                        selected_piece = self.board.game_state[start_pos[1]][start_pos[0]]

                        # If object is white piece
                        # display its moves on the board
                        if selected_piece and selected_piece.color == "white":
                            moves = selected_piece.get_moves(start_pos, self.board.game_state)

                            self.board.draw_moves(moves)
                            selected = True

                    elif selected == True:
                        # Get position of mouse click
                        end_pos = ((list(pygame.mouse.get_pos())[0] - BOARD_OFFSET) // SQSIZE, # xpos
                                   (list(pygame.mouse.get_pos())[1] - BOARD_OFFSET) // SQSIZE) # ypos

                        # Get object at that position
                        selected_piece = self.board.game_state[end_pos[1]][end_pos[0]]

                        # If object selected is another white piece
                        # Display its moves on the board
                        if selected_piece and selected_piece.color == "white":
                            moves = selected_piece.get_moves(end_pos, self.board.game_state)

                            # Redraw board to show new moves
                            self.board.draw_board()
                            self.board.draw_moves(moves)

                            # Need to update starting position
                            start_pos = end_pos

                        # Second click was a valid square
                        elif end_pos in moves:
                            # Set white piece equal to that square
                            self.board.game_state[end_pos[1]][end_pos[0]] = self.board.game_state[start_pos[1]][start_pos[0]]

                            # Set white piece's old position to none
                            self.board.game_state[start_pos[1]][start_pos[0]] = None

                            selected = False 
                            self.board.draw_board()
                    
            # Updates the display to reflect changes
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.game_loop()
