import chess
import numpy as np

from board_representations import BoardRepresentation

class BitBoard(BoardRepresentation):

    def board_to_model_input(self, board):
        pieces_order = [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        board_input = np.zeros((12 * (self.num_previous_positions + 1), 8, 8), dtype=np.float32)

        # Fill initial position
        for i, piece in enumerate(pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[i, chess.square_rank(square), chess.square_file(square)] = 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[i + 6, chess.square_rank(square), chess.square_file(square)] = 1

        # Fill previous positions
        for k in range(self.num_previous_positions):
            if len(board.move_stack) > 0:
                last_move = board.peek()
                board.pop()
            else:
                break

            for i, piece in enumerate(pieces_order):
                for square in board.pieces(piece, chess.WHITE):
                    board_input[12 * (k + 1) + i, chess.square_rank(square), chess.square_file(square)] = 1
                for square in board.pieces(piece, chess.BLACK):
                    board_input[12 * (k + 1) + i + 6, chess.square_rank(square), chess.square_file(square)] = 1
        return board_input


    def input_to_board(self, board_input):
        pieces_order = [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        board = chess.Board()
        board.clear_board()

        for i, piece in enumerate(pieces_order):
            for rank in range(8):
                for file in range(8):
                    if board_input[i, rank, file] == 1:
                        square = chess.square(file, rank)
                        board.set_piece_at(square, chess.Piece(piece, chess.WHITE))
                    if board_input[i + 6, rank, file] == 1:
                        square = chess.square(file, rank)
                        board.set_piece_at(square, chess.Piece(piece, chess.BLACK))

        return board