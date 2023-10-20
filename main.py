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

                # Restructure the code below to:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    pos = ((list(pygame.mouse.get_pos())[0] - BOARD_OFFSET) // SQSIZE,
                           (list(pygame.mouse.get_pos())[1] - BOARD_OFFSET) // SQSIZE)
                    # object at that position
                    game_object = self.board.game_state[pos[1]][pos[0]]
                    # If not selected and white
                    if selected == False:
                        if game_object and game_object.color == "white":
                            start_pos = pos
                            # get moves 
                            moves = game_object.get_moves((pos), self.board.game_state)
                            # draw moves
                            self.board.draw_moves(moves)
                            # select is true
                            selected = True
                    # If selected and white
                    if selected == True:
                        if game_object and game_object.color == "white":
                            start_pos = pos
                            # get moves
                            moves = game_object.get_moves((pos), self.board.game_state)
                            # redraw board first
                            self.board.draw_board()
                            # draw moves
                            self.board.draw_moves(moves)
                        
                        # If selected and black
                        elif pos in moves:    
                            end_pos = pos
                            # set white piece to new pos
                            self.board.game_state[end_pos[1]][end_pos[0]] = self.board.game_state[start_pos[1]][start_pos[0]]
                            # update old pos to none
                            self.board.game_state[start_pos[1]][start_pos[0]] = None
                            # redraw board
                            self.board.draw_board()
                            # seletect is false
                            selected = False

            # Updates the display to reflect changes
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.game_loop()
