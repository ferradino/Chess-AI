import sys
import pygame

from board import Board
from const import FPS

class Main():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.board = Board()

    def gameLoop(self):
        # Draw the board and the pieces on it
        self.board.drawBoard()
        running = True

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

            # Updates the display to reflect changes
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.gameLoop()