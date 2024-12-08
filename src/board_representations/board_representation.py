import chess
import numpy as np

"""
BoardRepresentation:
Class to be extended on with alternative board representation types
After initialization, holds:
    * board - A chess.Board() object
    * num_previous_positions - The number of previous positions that will be held in the board representation 
"""
class BoardRepresentation:
    pieces_order = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING, chess.PAWN]

    def __init__(self, board, num_previous_positions):
        self.num_previous_positions = num_previous_positions
        pass
        
    def __str__(self):
        raise NotImplementedError("Implement the __str__() method which should display the current board within this board representation")

    def board_to_model_input(self, board):
        raise NotImplementedError("Implement the board_to_model_input() method which should convert the board from a chess.Board() object to a suitable input for your NN model")

    def model_input_to_board(self, model_input);
        raise NotImplementedError("Implement the board_to_model_input() method which should convert the board from a chess.Board() object to a suitable input for your NN model")
