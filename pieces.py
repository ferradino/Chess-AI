from const import *
import pygame
import os


# Base ChessPiece class that serves as a blueprint for all chess pieces.
class ChessPiece:
    def __init__(self, color, img):
        self.color = color  # Color of the piece (white or black).
        self.img = pygame.transform.scale(pygame.image.load(os.path.join('images', img)), (SQSIZE, SQSIZE))  # Load piece image and scale to size

    # Placeholder method for possible moves.
    # Specific piece classes will override this with their movement logic.
    def possible_moves(self, position):
        pass


# The Pawn class represents the Pawn chess piece.
class Pawn(ChessPiece):
    def __init__(self, color):
        img = "wp.png" if color == "white" else "bp.png"
        super().__init__(color, img)

    def possible_moves(self, position):
        x, y = position  # Extracting the row and column from the position.
        moves = []  # A list to store all possible moves.
        # If the pawn is white, it moves upwards (i.e., row increases).
        if self.color == "white":
            if y + 1 < 8:
                moves.append((x, y + 1))
            # Special move for pawn: It can move 2 steps on its first move.
            if y == 1:
                moves.append((x, y + 2))
        # For black pawns, the movement is downward (i.e., row decreases).
        else:
            if y - 1 >= 0:
                moves.append((x, y - 1))
            if y == 6:
                moves.append((x, y - 2))
        return moves  # Return the list of valid moves.


# The Rook class represents the Rook chess piece which moves in straight lines.
class Rook(ChessPiece):
    def __init__(self, color):
        self.img = "wR.png" if color == "white" else "bR.png"
        super().__init__(color, self.img)

    def possible_moves(self, position):
        x, y = position
        moves = []
        # Rook can move to any other position in its current row or column.
        for i in range(8):
            if i != x:  # Avoiding the current position.
                moves.append((i, y))
            if i != y:
                moves.append((x, i))
        return moves


# The Bishop class represents the Bishop chess piece.
class Bishop(ChessPiece):
    def __init__(self, color):
        img = "wB.png" if color == "white" else "bB.png"
        super().__init__(color, img)

    def possible_moves(self, position):
        x, y = position
        moves = []
        # The bishop can move any number of squares diagonally.
        for i in range(1, 8):
            # Top-right diagonal
            if x + i < 8 and y + i < 8:
                moves.append((x + i, y + i))
            # Bottom-left diagonal
            if x - i >= 0 and y - i >= 0:
                moves.append((x - i, y - i))
            # Top-left diagonal
            if x + i < 8 and y - i >= 0:
                moves.append((x + i, y - i))
            # Bottom-right diagonal
            if x - i >= 0 and y + i < 8:
                moves.append((x - i, y + i))
        return moves


# The Knight class represents the Knight chess piece.
class Knight(ChessPiece):
    def __init__(self, color):
        img = "wN.png" if color == "white" else "bN.png"
        super().__init__(color, img)

    # Defining all possible moves for a knight.
    MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def possible_moves(self, position):
        x, y = position
        moves = []
        # The knight can jump to any of the positions defined in MOVES.
        for dx, dy in Knight.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                moves.append((nx, ny))
        return moves


# The Queen class represents the Queen chess piece.
class Queen(ChessPiece):
    def __init__(self, color):
        img = "wQ.png" if color == "white" else "bQ.png"
        super().__init__(color, img)

    def possible_moves(self, position):
        # The queen can move like both a rook and a bishop.
        return Rook(self.color).possible_moves(position) + Bishop(
            self.color
        ).possible_moves(position)


# The King class represents the King chess piece.
class King(ChessPiece):
    def __init__(self, color):
        img = "wK.png" if color == "white" else "bK.png"
        super().__init__(color, img)

    # Defining all possible moves for a king.
    MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def possible_moves(self, position):
        x, y = position
        moves = []
        # The king can move one square in any direction.
        for dx, dy in King.MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                moves.append((nx, ny))
        return moves