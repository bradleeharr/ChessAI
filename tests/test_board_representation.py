import chess
import numpy as np

from src.board_representations.board_representation import BoardRepresentation
from src.board_representations.bitboard import BitBoard 
from src.board_representations.piecemap import PieceMap

def test_BoardRepresentation_init():
    prev_pos1 = 0
    prev_pos2 = 5

    board1 = BoardRepresentation(num_previous_positions = prev_pos1)
    board2 = BoardRepresentation(num_previous_positions = prev_pos2)

    assert board1.num_previous_positions == prev_pos1
    assert board2.num_previous_positions == prev_pos2


def test_BitBoard_0_previous_positions():
    bitboard = BitBoard(num_previous_positions=0)
    input_board = chess.Board()
    model_input = bitboard.board_to_model_input(input_board)
    reconverted_board = bitboard.model_input_to_board(model_input)
    

    model_input_shape = np.shape(model_input)
    expected_shape = np.array((1, 12, 8, 8))
    assert np.all(model_input_shape == expected_shape) 

    print(reconverted_board)
    print("===============")
    print(input_board)
    print("===============")
    print(model_input)

    assert reconverted_board == input_board  


def test_PieceMap_0_previous_positions():
    piecemap = PieceMap(num_previous_positions=0)
    input_board = chess.Board()
    model_input = piecemap.board_to_model_input(input_board)
    reconverted_board = piecemap.model_input_to_board(model_input)

    model_input_shape = np.shape(model_input)
    expected_shape = np.array((1, 8, 8))

    print(model_input_shape)

    assert np.all(model_input_shape == expected_shape)
    assert reconverted_board == input_board


def test_BitBoard_5_previous_positions():
    input_board = chess.Board()
    moves = ['e4', 'e5', 'Qh5', 'Nc6', 'Bc4', 'Nf6', 'Qxf7']
    for moven in moves:
        input_board.push_san(moven)
    
    PLY = 5
    bitboard = BitBoard(num_previous_positions=PLY)
    model_input = bitboard.board_to_model_input(input_board)
    reconverted_board = bitboard.model_input_to_board(model_input)

    model_input_shape = np.shape(model_input)
    expected_shape = np.array((PLY+1, 12, 8, 8))

    assert np.all(model_input_shape == expected_shape) 
    assert input_board.ply() >= PLY
    assert reconverted_board == input_board
    

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