import chess
import numpy as np

from src.board_representations.bitboard import BitBoard 

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
    
