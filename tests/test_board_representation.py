import chess
import numpy as np

from src.board_representations.board_representation import BoardRepresentation
from src.board_representations.bitboard import BitBoard 
from src.board_representations.piecemap import PieceMap

def test_BitBoard_init():
    prev_pos1 = 0
    prev_pos2 = 5

    board1 = BoardRepresentation(num_previous_positions = prev_pos1)
    board2 = BoardRepresentation(num_previous_positions = prev_pos2)

    assert board1.num_previous_positions == prev_pos1
    assert board2.num_previous_positions == prev_pos2
    

# Tests that the 2d input conversion board method will convert the position to the board
def test_BitBoard_0_previous_positions():
    bitboard = BitBoard(num_previous_positions=0)

    input_board = chess.Board()
    model_input = bitboard.board_to_model_input(input_board)
    reconverted_board = bitboard.model_input_to_board(model_input)
    
    
    assert np.size(model_input) == np.array((8,8,7))
    assert reconverted_board == input_board  

# Tests that the 2d input conversion board method will convert the position in cases where depth is kept
def test_PieceMap_0_previous_positions():
    piecemap = PieceMap(num_previous_positions=0)

    input_board = chess.Board()
    model_input = piecemap.board_to_model_input(input_board)
    reconverted_board = piecemap.model_input_to_board(model_input)

    assert np.size(model_input) == np.array((8,8))
    assert reconverted_board == input_board

    """PLY = 5
    board = chess.Board()
    moves = ['e4', 'e5', 'Qh5', 'Nc6', 'Bc4', 'Nf6', 'Qxf7']
    for moven in moves:
        board.push_san(moven)

    input_board = board_to_input_2d(board, PLY)
    reconverted_board = input_to_board_2d(input_board, PLY)

    assert reconverted_board.ply() == PLY
    assert board.ply() >= PLY
    assert reconverted_board == board
    """
    

"""def test_move_to_flat():
    board = chess.Board()
    from_square, to_square = ('e2', 'e4')
    move = chess.Move.from_uci(from_square + to_square)
    flat = move_to_flat(move)
    unflat_move = flat_to_move(flat, board)
    
    print(move)
    print(flat)
    print(unflat_move)
    assert unflat_move == move
"""