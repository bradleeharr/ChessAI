import pytest
import chess

from from_colab import *
from from_colab.utilities import *


# Tests that the 2d input conversion board method will convert the position to the board
def test_board_to_2d_input_0_previous_positions():
    board = chess.Board()
    input_board = board_to_input_2d(board, 0)
    reconverted_board = input_to_board_2d(input_board, 0)

    print(board)
    print(input_board)
    print(reconverted_board)
    assert reconverted_board == board  

# Tests that the 2d input conversion board method will convert the position in cases where depth is kept
def test_board_to_2d_input_5_previous_positions():
    PLY = 5
    board = chess.Board()
    moves = ['e4', 'e5', 'Qh5', 'Nc6', 'Bc4', 'Nf6', 'Qxf7']
    for moven in moves:
        board.push_san(moven)

    input_board = board_to_input_2d(board, PLY)
    reconverted_board = input_to_board_2d(input_board, PLY)

    assert reconverted_board.ply() == PLY
    assert board.ply() >= PLY
    assert reconverted_board == board
    
    
def test_move_to_flat():
    board = chess.Board()
    from_square, to_square = ('e2', 'e4')
    move = chess.Move.from_uci(from_square + to_square)
    flat = move_to_flat(move)
    unflat_move = flat_to_move(flat, board)
    
    print(move)
    print(flat)
    print(unflat_move)
    assert unflat_move == move
