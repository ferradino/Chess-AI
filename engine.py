from pieces import *

class GameState:
    def __init__(self):
        # Initial setup of the chessboard with pieces in their starting positions.
        # Game board stored as an array of piece objects
        self.board = [
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

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = None
        self.board[move.end_row][move.end_col] = move.piece_moved

        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players

        # update king's location if moved
        if move.piece_moved == King and move.piece_moved.color == "white":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == King and move.piece_moved.color == "black":
            self.black_king_location = (move.end_row, move.end_col)

        # Check if Pawn Promotion
        if move.pawn_promotion:
            while True:
                promoted_piece = input("Promote to q, r, b, or k: ")
                if promoted_piece == "q":
                    promoted_piece = Queen(move.piece_moved.color)
                    break
                elif promoted_piece == "r":
                    promoted_piece = Rook(move.piece_moved.color)
                    break
                elif promoted_piece == "b":
                    promoted_piece = Bishop(move.piece_moved.color)
                    break
                elif promoted_piece == "k":
                    promoted_piece = Knight(move.piece_moved.color)
                    break
                else:
                    print("Not a valid piece, please reselect!")

            self.board[move.end_row][move.end_col] = promoted_piece

class Move:
    def __init__(self, start_square, end_sqaure, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]

        self.end_row = end_sqaure[0]
        self.end_col = end_sqaure[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_capture = self.piece_captured != None

        self.pawn_promotion = type(self.piece_moved) == Pawn and self.end_row in (0,7)
