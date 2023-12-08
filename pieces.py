from const import SQSIZE
import pygame
import os


# Base ChessPiece class that serves as a blueprint for all chess pieces.
class ChessPiece:
    def __init__(self, color, img):
        self.color = color  # Color of the piece (white or black).
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("images", img)), (SQSIZE, SQSIZE)
        )  # Load piece image and scale to size

def is_in_check(self, color, board_changes = None): 
        output = False
        kings_position = None
        next_piece = None
        block = None
        new_block = None
        new_block2 = None
        if board_changes is not None:
            for square in self.squares:
                if square.pos == board_changes[0]:
                    next_piece = square.occupying_piece
                    block = square
                    block.occupying_piece = None
            for square in self.squares:
                if square.pos == board_changes[1]:
                    new_block = square
                    new_block2 = new_block.occupying_piece
                    new_block.occupying_piece = next_piece
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        if next_piece is not None:
            if next_piece.notation == 'K':
                kings_position = new_block.pos
        if kings_position == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                        kings_position = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == kings_position:
                        output = True
        if board_changes is not None:
            block.occupying_piece = next_piece
            new_block.occupying_piece = new_block2
        return output

def is_in_checkmate(self, color):
        output = False
        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece
        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                output = True
        return output

# The Pawn class represents the Pawn chess piece.
class Pawn(ChessPiece):
    def __init__(self, color):
        img = "wp.png" if color == "white" else "bp.png"
        super().__init__(color, img)
        self.just_moved_two_squares = False  # New attribute to track two-square moves

    def get_moves(self, position, board, last_move):
        x, y = position  # Extracting the row and column from the position.
        moves = []  # A list to store all possible moves.

        # En passant logic
        if last_move is not None and isinstance(last_move.piece_moved, Pawn):
            if last_move.piece_moved.just_moved_two_squares:
                if self.color == "black" and y == 4:
                    if last_move.end_col == x - 1:  # En passant capture to the left
                        moves.append((x - 1, y + 1))
                    elif last_move.end_col == x + 1:  # En passant capture to the right
                        moves.append((x + 1, y + 1))
                elif self.color == "white" and y == 3:
                    if last_move.end_col == x - 1:  # En passant capture to the left
                        moves.append((x - 1, y - 1))
                    elif last_move.end_col == x + 1:  # En passant capture to the right
                        moves.append((x + 1, y - 1))

        if self.color == "black":
            if y + 1 < 8:
                if board[y + 1][x] == None:
                    moves.append((x, y + 1))
                if x - 1 >= 0:
                    if board[y + 1][x - 1] != None:
                        if board[y + 1][x - 1].color != self.color:
                            moves.append((x - 1, y + 1))
                if x + 1 <= 7:
                    if board[y + 1][x + 1] != None:
                        if board[y + 1][x + 1].color != self.color:
                            moves.append((x + 1, y + 1))
            # Special move for pawn: It can move 2 steps on its first move.
            if y == 1 and (board[y + 1][x] == board[y + 2][x] == None):
                moves.append((x, y + 2))
        # For white pawns, the movement is upward (i.e., row decreases).
        else:
            if y - 1 >= 0:
                if board[y - 1][x] == None:
                    moves.append((x, y - 1))
                if x - 1 >= 0:
                    if board[y - 1][x - 1] != None:
                        if board[y - 1][x - 1].color != self.color:
                            moves.append((x - 1, y - 1))
                if x + 1 <= 7:
                    if board[y - 1][x + 1] != None:
                        if board[y - 1][x + 1].color != self.color:
                            moves.append((x + 1, y - 1))
            if y == 6 and (board[y - 1][x] == board[y - 2][x] == None):
                moves.append((x, y - 2))

        return moves  # Return the list of valid moves.


# The Rook class represents the Rook chess piece which moves in straight lines.
class Rook(ChessPiece):
    def __init__(self, color):
        self.img = "wR.png" if color == "white" else "bR.png"
        self.has_moved = False
        super().__init__(color, self.img)

    DIRS = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    def get_moves(self, position, board, last_move=None):
        x, y = position
        moves = []

        for move in Rook.DIRS:
            for i in range(1, 8):
                rx, ry = x + (i * move[0]), y + (i * move[1])
                if (rx >= 0 and rx <= 7) and (ry >= 0 and ry <= 7):
                    if board[ry][rx] == None:
                        moves.append((rx, ry))
                    elif board[ry][rx].color != self.color:
                        moves.append((rx, ry))
                        break
                    else:
                        break
                else:
                    break

        return moves


# The Bishop class represents the Bishop chess piece.
class Bishop(ChessPiece):
    def __init__(self, color):
        img = "wB.png" if color == "white" else "bB.png"
        super().__init__(color, img)

    DIRS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]

    def get_moves(self, position, board, last_move=None):
        x, y = position
        moves = []

        for move in Bishop.DIRS:
            for i in range(1, 8):
                bx, by = x + (i * move[0]), y + (i * move[1])
                if (bx >= 0 and bx <= 7) and (by >= 0 and by <= 7):
                    if board[by][bx] == None:
                        moves.append((bx, by))
                    elif board[by][bx].color != self.color:
                        moves.append((bx, by))
                        break
                    else:
                        break
                else:
                    break

        return moves


# The Knight class represents the Knight chess piece.
class Knight(ChessPiece):
    def __init__(self, color):
        img = "wN.png" if color == "white" else "bN.png"
        super().__init__(color, img)

    # Defining all possible moves for a knight.
    DIRS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def get_moves(self, position, board, last_move=None):
        x, y = position
        moves = []
        # The knight can jump to any of the positions defined in DIRS.
        for move in Knight.DIRS:
            nx, ny = x + move[0], y + move[1]
            if (nx >= 0 and nx <= 7) and (ny >= 0 and ny <= 7):
                if board[ny][nx] == None or board[ny][nx].color != self.color:
                    moves.append((nx, ny))

        return moves


# The Queen class represents the Queen chess piece.
class Queen(ChessPiece):
    def __init__(self, color):
        img = "wQ.png" if color == "white" else "bQ.png"
        super().__init__(color, img)

    def get_moves(self, position, board, last_move=None):
        # The queen can move like both a rook and a bishop.
        return Rook(self.color).get_moves(position, board) + Bishop(
            self.color
        ).get_moves(position, board)


# The King class represents the King chess piece.
class King(ChessPiece):
    def __init__(self, color):
        img = "wK.png" if color == "white" else "bK.png"
        self.has_moved = False
        super().__init__(color, img)

    # Defining all possible moves for a king.
    DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def check_for_castle(self, position, board, moves):
        y = position[1]

        # check if king moved
        if self.has_moved == False:
            # check queen side castling
            if type(board[y][0]) == Rook and board[y][0].color == self.color:
                if board[y][0].has_moved == False:
                    # Check if all slots are empty
                    if board[y][1] == board[y][2] == board[y][3] == None:
                        # Add to move list
                        moves.append((0, y))

            # check king side castling
            if type(board[y][7]) == Rook and board[y][7].color == self.color:
                if board[y][7].has_moved == False:
                    # Check if all slots are empty
                    if board[y][6] == board[y][5] == None:
                        # Add to move list
                        moves.append((7, y))

    def get_moves(self, position, board, last_move=None):
        x, y = position
        moves = []
        # The king can move one square in any direction.
        for move in King.DIRS:
            kx, ky = x + move[0], y + move[1]
            if (ky >= 0 and kx <= 7) and (ky >= 0 and ky <= 7):
                if board[ky][kx] == None or board[ky][kx].color != self.color:
                    moves.append((kx, ky))

        self.check_for_castle(position, board, moves)

        return moves
