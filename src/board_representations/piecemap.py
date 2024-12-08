
import chess
import numpy as np

from src.board_representations.board_representation import BoardRepresentation


class PieceMap(BoardRepresentation):
    # TODO: Currently only uses single ply -- "num_previous_positions" is redundant
    def board_to_model_input(self, board):
        board_input = np.zeros((8, 8, self.num_previous_positions + 1), dtype=int)

        for i, piece in enumerate(self.pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = i + 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = -(i + 1)

        return board_input

    def model_input_to_board(self, model_input):
        board = chess.Board()
        board.clear_board()
        for rank in range(8):
            for file in range(8):
                piece = model_input[rank, file, 0]
                if piece == 0:
                    continue
                color = chess.WHITE if piece > 0 else chess.BLACK
                piece_type = self.pieces_order[abs(piece) - 1]
                square = chess.square(file, rank)
                board.set_piece_at(square, chess.Piece(piece_type, color))
        
        return board