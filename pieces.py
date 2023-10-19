from const import *
import pygame
import os

# Base ChessPiece class that serves as a blueprint for all chess pieces.
class ChessPiece:
    def __init__(self, color, img):
        self.color = color  # Color of the piece (white or black).
        self.img = pygame.transform.scale(pygame.image.load(os.path.join('images', img)), (SQSIZE, SQSIZE))  # Load piece image and scale to size

    # Placeholder method for possible getMoves.
    # Specific piece classes will override this with their movement logic.
    def getMoves(self, position):
        pass

# The Pawn class represents the Pawn chess piece.
class Pawn(ChessPiece):
    def __init__(self, color):
        img = "wp.png" if color == "white" else "bp.png"
        super().__init__(color, img)

    def getMoves(self, position):
        x, y = position  # Extracting the row and column from the position.
        getMoves = []  # A list to store all possible getMoves.
        # If the pawn is white, it getMoves upwards (i.e., row increases).
        if self.color == "black":
            if y + 1 < 8:
                getMoves.append((x, y + 1))
            # Special move for pawn: It can move 2 steps on its first move.
            if y == 1:
                getMoves.append((x, y + 2))
        # For black pawns, the movement is downward (i.e., row decreases).
        else:
            if y - 1 >= 0:
                getMoves.append((x, y - 1))
            if y == 6:
                getMoves.append((x, y - 2))
        return getMoves  # Return the list of valid getMoves.


# The Rook class represents the Rook chess piece which getMoves in straight lines.
class Rook(ChessPiece):
    def __init__(self, color):
        self.img = "wR.png" if color == "white" else "bR.png"
        super().__init__(color, self.img)

    def getMoves(self, position):
        x, y = position
        getMoves = []
        # Rook can move to any other position in its current row or column.
        for i in range(8):
            if i != x:  # Avoiding the current position.
                getMoves.append((i, y))
            if i != y:
                getMoves.append((x, i))
        return getMoves


# The Bishop class represents the Bishop chess piece.
class Bishop(ChessPiece):
    def __init__(self, color):
        img = "wB.png" if color == "white" else "bB.png"
        super().__init__(color, img)

    def getMoves(self, position):
        x, y = position
        getMoves = []
        # The bishop can move any number of squares diagonally.
        for i in range(1, 8):
            # Top-right diagonal
            if x + i < 8 and y + i < 8:
                getMoves.append((x + i, y + i))
            # Bottom-left diagonal
            if x - i >= 0 and y - i >= 0:
                getMoves.append((x - i, y - i))
            # Top-left diagonal
            if x + i < 8 and y - i >= 0:
                getMoves.append((x + i, y - i))
            # Bottom-right diagonal
            if x - i >= 0 and y + i < 8:
                getMoves.append((x - i, y + i))
        return getMoves


# The Knight class represents the Knight chess piece.
class Knight(ChessPiece):
    def __init__(self, color):
        img = "wN.png" if color == "white" else "bN.png"
        super().__init__(color, img)

    # Defining all possible getMoves for a knight.
    MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def getMoves(self, position):
        x, y = position
        getMoves = []
        # The knight can jump to any of the positions defined in MOVES.
        for dx, dy in Knight.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                getMoves.append((nx, ny))
        return getMoves


# The Queen class represents the Queen chess piece.
class Queen(ChessPiece):
    def __init__(self, color):
        img = "wQ.png" if color == "white" else "bQ.png"
        super().__init__(color, img)

    def getMoves(self, position):
        # The queen can move like both a rook and a bishop.
        return Rook(self.color).getMoves(position) + Bishop(
            self.color
        ).getMoves(position)


# The King class represents the King chess piece.
class King(ChessPiece):
    def __init__(self, color):
        img = "wK.png" if color == "white" else "bK.png"
        super().__init__(color, img)

    # Defining all possible getMoves for a king.
    MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def getMoves(self, position):
        x, y = position
        getMoves = []
        # The king can move one square in any direction.
        for dx, dy in King.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                getMoves.append((nx, ny))
        return getMoves
