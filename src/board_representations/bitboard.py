import chess
import numpy as np

from board_representations.board_representation import BoardRepresentation

class BitBoard(BoardRepresentation):
    def __init__(self, num_previous_positions):
        super().__init__(num_previous_positions)
        self.in_channels = (num_previous_positions + 1)*12


    def board_to_model_input(self, board):
        pieces_order = [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        board_input = np.zeros(
            (self.num_previous_positions+1, 12, 8, 8),
            dtype=np.float32
        )

        for i, piece in enumerate(pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[0, i, chess.square_rank(square), chess.square_file(square)] = 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[0, i + 6, chess.square_rank(square), chess.square_file(square)] = 1

        for k in range(self.num_previous_positions):
            if len(board.move_stack) > 0:
                last_move = board.peek()
                board.pop()
            else:
                break

            for i, piece in enumerate(pieces_order):
                for square in board.pieces(piece, chess.WHITE):
                    board_input[k, i, chess.square_rank(square), chess.square_file(square)] = 1
                for square in board.pieces(piece, chess.BLACK):
                    board_input[k, i + 6, chess.square_rank(square), chess.square_file(square)] = 1
        return board_input


    def model_input_to_board(self, model_input):
        pieces_order = [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        board = chess.Board()
        board.clear_board()

        for k in range(self.num_previous_positions+1):
            for i, piece in enumerate(pieces_order):
                for rank in range(8):
                    for file in range(8):
                        if model_input[k, i, rank, file] == 1:
                            square = chess.square(file, rank)
                            board.set_piece_at(square, chess.Piece(piece, chess.WHITE))
                        if model_input[k, i + 6, rank, file] == 1:
                            square = chess.square(file, rank)
                            board.set_piece_at(square, chess.Piece(piece, chess.BLACK))
        

        return board