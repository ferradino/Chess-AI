import numpy as np
from pieces import *
from const import ROWS, COLS

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

# Our model we trained from the ai
model = "model.keras"  # Change this to use a different model from the models folder
model = tf.keras.models.load_model(os.path.join("models", model))


class GameState:
    def __init__(self):
        self.last_move = None
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
        # Update the board with the new move
        self.board[move.start_row][move.start_col] = None
        self.board[move.end_row][move.end_col] = move.piece_moved

        # En passant logic
        if isinstance(move.piece_moved, Pawn) and move.is_enpassant:
            direction = -1 if move.piece_moved.color == "white" else 1
            # Correctly removing the captured pawn
            self.board[move.end_row - direction][move.end_col] = None

        # Handle the two-square pawn move for en passant
        if (
            isinstance(move.piece_moved, Pawn)
            and abs(move.start_row - move.end_row) == 2
        ):
            move.piece_moved.just_moved_two_squares = True
        else:
            # Reset the flag for all pawns
            for row in self.board:
                for piece in row:
                    if isinstance(piece, Pawn):
                        piece.just_moved_two_squares = False

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

        # Log the move and switch players
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        # Update king's and rook's location if moved, and set their has_moved attribute
        if isinstance(move.piece_moved, King):
            if move.piece_moved.color == "white":
                self.white_king_location = (move.end_row, move.end_col)
            else:
                self.black_king_location = (move.end_row, move.end_col)
            move.piece_moved.has_moved = True
        elif isinstance(move.piece_moved, Rook):
            move.piece_moved.has_moved = True

        # Check if Pawn Promotion
        if move.pawn_promotion:
            # Pawn promotion logic here
            pass

        # Update last move
        self.last_move = move

    # Undo the last move made
    # Resets all changes to gamestate from previous move
    def undo_move(self):
        # get the last move made
        move = self.move_log[len(self.move_log) - 1]

        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured

        if type(move.piece_moved) == King and move.piece_moved.color == "white":
            self.white_king_location = (move.start_row, move.start_col)
            self.board[move.start_row][
                move.start_col
            ].has_moved = False  # Set has_moved attribute to false
        elif type(move.piece_moved) == King and move.piece_moved.color == "black":
            self.black_king_location = (move.start_row, move.start_col)
            self.board[move.start_row][
                move.start_col
            ].has_moved = False  # Set has_moved attribute to false

        if type(move.piece_moved) == Rook:
            self.board[move.start_row][move.start_col].has_moved = False

        # Check if castle
        if move.is_castle:
            # Check which side the castle is
            if abs(move.start_col - move.end_col) == 3:
                # King side castle
                self.board[move.end_row][6] = None
                self.board[move.end_row][5] = None
                self.board[move.start_row][move.start_col] = King(
                    move.piece_moved.color
                )
                self.board[move.end_row][move.end_col] = Rook(move.piece_moved.color)
            elif abs(move.start_col - move.end_col) == 4:
                # Queen side castle
                self.board[move.end_row][2] = None
                self.board[move.end_row][3] = None
                self.board[move.start_row][move.start_col] = King(
                    move.piece_moved.color
                )
                self.board[move.end_row][move.end_col] = Rook(move.piece_moved.color)

        # check if last move was checkmate
        self.checkmate = False if self.checkmate else self.checkmate
        self.stalemate = False if self.stalemate else self.stalemate

        self.white_to_move = not self.white_to_move

        # pop move log
        self.move_log.pop()

    # Get all the possible moves for a certain color pieces
    def get_all_possible_moves(self, color):
        legal_moves = []
        moves = []

        # Loop through each row and column looking for a piece
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(self.board[y][x], ChessPiece) and piece.color == color:
                    # Get all possible moves that piece found
                    moves = piece.get_moves((x, y), self.board, self.last_move)
                    for move in moves:
                        legal_moves.append(
                            Move((y, x), (move[1], move[0]), self.board, self.last_move)
                        )
        return legal_moves

    def convert_to_3d(self, board):
        # this is our board represented in a 3d array
        board3d = np.zeros((14, 8, 8), dtype=np.int8)

        # all possible piece types
        pieces = [Pawn, Knight, Bishop, Rook, Queen, King]

        # looking for instance of each piece type on board
        # will append a one to the 3d array if that piece exists on board
        i = 0
        for piece in pieces:
            for row in range(ROWS):
                for col in range(COLS):
                    if (
                        type(board[row][col]) == piece
                        and board[row][col].color == "white"
                    ):
                        board3d[i][row][col] = 1

            for row in range(ROWS):
                for col in range(COLS):
                    if (
                        type(board[row][col]) == piece
                        and board[row][col].color == "black"
                    ):
                        board3d[i + 6][row][col] = 1
            i += 1

        # get all the attacking square for white and black
        white_moves = self.get_all_possible_moves("white")
        for move in white_moves:
            board3d[12][move.end_row][move.end_col] = 1

        black_moves = self.get_all_possible_moves("black")
        for move in black_moves:
            board3d[13][move.end_row][move.end_row] = 1

        return board3d

    # Write a Min/Max evaluation to turn model into an array we can work with
    def get_board_eval(self):
        # Turn our board into a board the model can understand
        board3d = self.convert_to_3d(self.board)
        board3d = np.expand_dims(board3d, 0)

        # Return the evaluation from the model
        eval = model.predict(board3d)
        return float(eval[0][0])

    # Write a Min/Max fuction
    def minimax(self, depth, a, b, max):
        # Hit final depth or game is over
        if depth == 0:
            return self.get_board_eval()

        # If turn is black
        if max:
            max_eval = -np.inf
            for move in self.get_all_possible_moves("black"):
                # Make move
                self.make_move(move)

                # Evaluate the move
                eval = self.minimax(depth - 1, a, b, False)

                # Undo move
                self.undo_move()

                # Get max eval
                max_eval = np.maximum(max_eval, eval)
                a = np.maximum(a, eval)
                if b <= a:
                    break

            # Return max eval (or best move for black)
            return max_eval

        # If turn is white
        else:
            min_eval = np.inf
            for move in self.get_all_possible_moves("white"):
                # Make move
                self.make_move(move)

                # Evaluate the move
                eval = self.minimax(depth - 1, a, b, True)

                # Undo move
                self.undo_move()

                # Get min eval (or best move for white)
                min_eval = np.minimum(min_eval, eval)
                b = np.minimum(b, eval)
                if b <= a:
                    break

            # Return min eval (or best move for white)
            return min_eval

    # Write function to get AI move
    def ai_move(self, depth=1):
        best_move = None
        max_eval = -np.inf

        # Loop through, evaluating each move
        for move in self.get_all_possible_moves("white"):
            # Make move
            self.make_move(move)

            # Evaluate the move
            eval = self.minimax(depth - 1, -np.inf, np.inf, False)

            # Undo move
            self.undo_move()

            # Get max evaluation
            if eval > max_eval:
                max_eval = eval
                best_move = move

        # return best move
        return best_move


class Move:
    def __init__(self, start_square, end_sqaure, board, last_move):
        self.start_row = start_square[0]
        self.start_col = start_square[1]

        self.end_row = end_sqaure[0]
        self.end_col = end_sqaure[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_capture = self.piece_captured != None

        self.pawn_promotion = type(self.piece_moved) == Pawn and self.end_row in (0, 7)
        self.is_enpassant = False

        self.is_castle = type(self.piece_moved) == King and (
            type(self.piece_captured) == Rook
            and self.piece_captured.color == self.piece_moved.color
        )

        # En passant logic
        if isinstance(self.piece_moved, Pawn):
            if abs(self.start_col - self.end_col) == 1 and self.piece_captured is None:
                # Additional checks for en passant
                if (
                    last_move
                    and isinstance(last_move.piece_moved, Pawn)
                    and last_move.piece_moved.just_moved_two_squares
                ):
                    if (
                        last_move.end_row == self.start_row
                        and last_move.end_col == self.end_col
                    ):
                        self.is_enpassant = True
