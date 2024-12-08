
import chess
import numpy as np

from from_colab.board_representations import BoardRepresentation



class PieceMapBoardRepresentation(BoardRepresentation):
    """
    Represents a Board Representation using a Map of Pieces
    """
    # TODO: Currently only uses single ply -- "num_previous_positions" is redundant
    def to_model_input(self, board):
        pieces_order = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING, chess.PAWN]
        board_input = np.zeros((8, 8, self.num_previous_positions + 1), dtype=int)

        for i, piece in enumerate(pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = i + 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = -(i + 1)

        return board_input

    def set_board_from_model_input(self, model_input):
        pieces_order = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING, chess.PAWN]
        board = chess.Board()
        board.clear_board()
        for rank in range(8):
            for file in range(8):
                piece = model_input[rank, file, 0]
                if piece == 0:
                    continue
                color = chess.WHITE if piece > 0 else chess.BLACK
                piece_type = pieces_order[abs(piece) - 1]
                square = chess.square(file, rank)
                board.set_piece_at(square, chess.Piece(piece_type, color))
        
        self.board = board