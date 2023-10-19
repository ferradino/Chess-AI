from const import *
import pygame
import os

# Base ChessPiece class that serves as a blueprint for all chess pieces.
class ChessPiece:
    def __init__(self, color, img):
        self.color = color  # Color of the piece (white or black).
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("images", img)), (SQSIZE, SQSIZE)
        )  # Load piece image and scale to size

    # Placeholder method for possible moves.
    # Specific piece classes will override this with their movement logic.
    def moves(self, position):
        pass

""" TODO: Implement Pawn Capture """
# The Pawn class represents the Pawn chess piece.
class Pawn(ChessPiece):
    def __init__(self, color):
        img = "wp.png" if color == "white" else "bp.png"
        super().__init__(color, img)

    def get_moves(self, position, board):
        x, y = position  # Extracting the row and column from the position.
        moves = []  # A list to store all possible moves.
        # If the pawn is white, it moves upwards (i.e., row increases).
        if self.color == "black":
            if y + 1 < 8 and board[y+1][x] == None:
                moves.append((x, y + 1))
            # Special move for pawn: It can move 2 steps on its first move.
            if y == 1 and None in { board[y+1][x], board[y+2][x] }:
                moves.append((x, y + 2))
        # For black pawns, the movement is downward (i.e., row decreases).
        else:
            if y - 1 >= 0 and board[y-1][x] == None:
                moves.append((x, y - 1))
            if y == 6 and None in { board[y-1][x], board[y-2][x] }:
                moves.append((x, y - 2))

            # Pawn Promotion logic
        if self.color == "white" and y == 0:
            board.promote_pawn(x, y)
        elif self.color == "black" and y == 7:
            board.promote_pawn(x, y)

            # En Passant
        """
        if board.last_move:
            last_piece_moved, last_start, last_end = board.last_move
            if (
                isinstance(last_piece_moved, Pawn)
                and abs(last_start[1] - last_end[1]) == 2
            ):
                if self.color == "white" and y == 3:
                    if x - 1 == last_end[0] or x + 1 == last_end[0]:
                        moves.append((last_end[0], last_end[1] - 1))
                elif self.color == "black" and y == 4:
                    if x - 1 == last_end[0] or x + 1 == last_end[0]:
                        moves.append((last_end[0], last_end[1] + 1))
        """

        return moves  # Return the list of valid moves.

# The Rook class represents the Rook chess piece which moves in straight lines.
class Rook(ChessPiece):
    def __init__(self, color):
        self.img = "wR.png" if color == "white" else "bR.png"
        self.has_moved = False
        super().__init__(color, self.img)

    def get_moves(self, position, board):
        x, y = position
        moves = []

        # Check all moves up
        for i in range(y-1, -1, -1):
            if board[i][x] == None:
                moves.append((x, i))
            elif board[i][x].color == "black":
                moves.append((x, i))
                break
            else:
                break
        # Check all moves down 
        for i in range(y+1, 8):
            if board[i][x] == None:
                moves.append((x, i))
            elif board[i][x].color == "black":
                moves.append((x, i))
                break
            else:
                break
        # Check all moves to the left
        for i in range(x-1, -1, -1):
            if board[y][i] == None:
                moves.append((i, y))
            elif board[y][i].color == "black":
                moves.append((i, y))
                break
            else:
                break
        # Check all moves to the right
        for i in range(x+1, 8):
            if board[y][i] == None: 
                moves.append((i, y))
            elif board[y][i].color == "black":
                moves.append((i, y))
                break
            else:
                break

        return moves

# The Bishop class represents the Bishop chess piece.
class Bishop(ChessPiece):
    def __init__(self, color):
        img = "wB.png" if color == "white" else "bB.png"
        super().__init__(color, img)

    def get_moves(self, position, board):
        x, y = position
        moves = []

        # Check moves top-left
        for i in range(1, 8):
            if (x - i >= 0 and y - i >= 0):
                if board[y-i][x-i] == None: 
                    moves.append((x-i, y-i))
                elif board[y-i][x-i].color == "black":
                    moves.append((x-i, y-i))
                    break
                else:
                    break
            else:
                break
        # Check moves top-right
        for i in range(1, 8):
            if (x + i < 8 and y - i >= 0):
                if board[y-i][x+i] == None:
                    moves.append((x+i, y-i))
                elif board[y-i][x+i].color == "black":
                    moves.append((x+i, y-i))
                    break
                else:
                    break
            else:
                break
        # Check moves bottom-left
        for i in range(1, 8):
            if (x - i >= 0 and y + i < 8):
                if board[y+i][x-i] == None:
                    moves.append((x-i, y+i))
                elif board[y+i][x-i].color == "black":
                    moves.append((x-i, y+i))
                    break
                else:
                    break
            else:
                break
        # Check moves bottom_right
        for i in range(1, 8):
            if (x + i < 8 and y + i < 8):
                if board[y+i][x+i] == None:
                    moves.append((x+i, y+i))
                elif board[y+i][x+i].color == "black":
                    moves.append((x+i, y+i))
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
    MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def get_moves(self, position, board):
        x, y = position
        moves = []
        # The knight can jump to any of the positions defined in MOVES.
        for move in Knight.MOVES:
            nx, ny = x + move[0], y + move[1]
            if (nx >= 0 and nx <= 7) and (ny >= 0 and ny <= 7):
                if board[ny][nx] == None or board[ny][nx].color == "black":
                    moves.append((nx, ny))

        return moves

# The Queen class represents the Queen chess piece.
class Queen(ChessPiece):
    def __init__(self, color):
        img = "wQ.png" if color == "white" else "bQ.png"
        super().__init__(color, img)

    def get_moves(self, position, board):
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
    MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def get_moves(self, position, board):
        x, y = position
        moves = []
        # The king can move one square in any direction.
        for move in King.MOVES:
            nx, ny = x + move[0], y + move[1] 
            if (ny >= 0 and nx <= 7) and (ny >= 0 and ny <= 7):
                if board[ny][nx] == None or board[ny][nx].color == "black":
                    moves.append((nx, ny))

        """
        # Castling logic
        if not self.has_moved and not board.is_in_check(self.color):
            # Check for king-side castling (O-O)
            if isinstance(board[y][7], Rook) and not board[y][7].has_moved:
                if not board[y][5] and not board[y][6]:
                    if not board.is_square_under_attack(
                        5, y, self.color
                    ) and not board.is_square_under_attack(6, y, self.color):
                        moves.append((6, y))

            # Check for queen-side castling (O-O-O)
            if isinstance(board[y][0], Rook) and not board[y][0].has_moved:
                if not board[y][1] and not board[y][2] and not board[y][3]:
                    if not board.is_square_under_attack(
                        3, y, self.color
                    ) and not board.is_square_under_attack(2, y, self.color):
                        moves.append((2, y))

        """

        return moves
