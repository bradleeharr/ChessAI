import chess
import numpy as np

from from_colab.board_representations import BoardRepresentation


class BitBoardBoardRepresentation(BoardRepresentation):
    
    def to_model_input(self, board):
        pieces_order = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING, chess.PAWN]
        board_input = np.zeros((8, 8, self.num_previous_positions + 1), dtype=int)

        # Fill initial position
        for i, piece in enumerate(pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = i + 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[chess.square_rank(square), chess.square_file(square), 0] = -(i + 1)

        return board_input


    def input_to_board_2d(board_input, self.num_previous_positions=0):
        pieces_order = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING, chess.PAWN]
        board = chess.Board()
        board.clear_board()
        for rank in range(8):
            for file in range(8):
                piece = board_input[rank, file, 0]
                if piece == 0:
                    continue
                color = chess.WHITE if piece > 0 else chess.BLACK
                piece_type = pieces_order[abs(piece) - 1]
                square = chess.square(file, rank)
                board.set_piece_at(square, chess.Piece(piece_type, color))
        return board

    # Converts a board to a 3D array suitable for the CNN input
    def board_to_input(board, num_previous_positions):
        pieces_order = [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING]
        board_input = np.zeros((12 * (num_previous_positions + 1), 8, 8), dtype=np.float32)

        # Fill initial position
        for i, piece in enumerate(pieces_order):
            for square in board.pieces(piece, chess.WHITE):
                board_input[i, chess.square_rank(square), chess.square_file(square)] = 1
            for square in board.pieces(piece, chess.BLACK):
                board_input[i + 6, chess.square_rank(square), chess.square_file(square)] = 1

        # Fill previous positions
        for k in range(num_previous_positions):
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


    def input_to_board(board_input, num_previous_positions=0):
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