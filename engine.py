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

        self.move_log.append(move)  # log the move 
        self.white_to_move = not self.white_to_move  # switch players

        # Update king's location if moved
        if type(move.piece_moved) == King and move.piece_moved.color == "white":
            self.white_king_location = (move.end_row, move.end_col)
            self.board[move.end_row][move.end_col].has_moved = True     # Set has_moved attribute to true
        elif type(move.piece_moved) == King and move.piece_moved.color == "black":
            self.black_king_location = (move.end_row, move.end_col)
            self.board[move.end_row][move.end_col].has_moved = True     # Set has_moved attribute to true

        # Check if piece moved was a Rook (Is not able to castle after it moves)
        if type(move.piece_moved) == Rook:
            self.board[move.end_row][move.end_col].has_moved = True

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

        # Check if En Passant
        if move.is_enpassant:
            pass

        # Check if castle
        if move.is_castle:
            # Check which side the castle is
            if abs(move.start_col - move.end_col) == 3:
                # King side castle
                self.board[move.end_row][6] = move.piece_moved
                self.board[move.end_row][5] = move.piece_captured
            elif abs(move.start_col - move.end_col) == 4:
                # Queen side castle
                self.board[move.end_row][2] = move.piece_moved
                self.board[move.end_row][3] = move.piece_captured
            else:
                print("Error: Shouldn't have been a castling move")

            # Reset the old rook position to None
            self.board[move.end_row][move.end_col] = None



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
        self.is_enpassant = False

        self.is_castle = type(self.piece_moved) == King and (type(self.piece_captured) == Rook and self.piece_captured.color == self.piece_moved.color)
