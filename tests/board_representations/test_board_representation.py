import chess
import numpy as np

from src.board_representations.board_representation import BoardRepresentation


def test_BoardRepresentation_init():
    prev_pos1 = 0
    prev_pos2 = 5

    board1 = BoardRepresentation(num_previous_positions = prev_pos1)
    board2 = BoardRepresentation(num_previous_positions = prev_pos2)

    assert board1.num_previous_positions == prev_pos1
    assert board2.num_previous_positions == prev_pos2




