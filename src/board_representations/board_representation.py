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
    def __init__(self, board, num_previous_positions):
        self.board = board
        self.num_previous_positions = num_previous_positions
        pass
        
    def __str__(self):
        raise NotImplementedError("Implement the __str__() method which should display the current board within this board representation")


    def to_input(self):
        raise NotImplementedError("Implement the to_input() method which should convert the board from a chess.Board() object to a suitable input for your NN model")
