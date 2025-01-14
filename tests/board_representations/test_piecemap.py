import chess
import numpy as np

from src.board_representations.piecemap import PieceMap

def test_PieceMap_0_previous_positions():
    piecemap = PieceMap(num_previous_positions=0)
    input_board = chess.Board()
    model_input = piecemap.board_to_model_input(input_board)
    reconverted_board = piecemap.model_input_to_board(model_input)

    model_input_shape = np.shape(model_input)
    expected_shape = np.array((1, 8, 8))

    [print(model_input_shape) for i in range(100) ]
    assert np.all(model_input_shape == expected_shape)
    assert reconverted_board == input_board