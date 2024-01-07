import numpy as np
from data.classes import BitboardUtility as bbu

class Bitboard:
    def __init__(self, pieces) -> None:
        self.pieces = pieces
        self.rep = {
            'P' : np.uint64(0),
            'Q' : np.uint64(0),
            'K' : np.uint64(0),
            'N' : np.uint64(0),
            'B' : np.uint64(0),
            'R' : np.uint64(0)
        }
        

    def initializeBB(self):
        for piece in self.pieces:
            file = piece.pos[0]
            rank = piece.pos[1]

            file_index = ord(file)- ord('a')
            rank_index = rank - 1

            piece_bb = self.rep[piece.notation]
        
            piece_bb |= bbu.FILES[file_index] & bbu.RANKS[rank_index]

            self.rep[piece.notation] = piece_bb
        
    def printBB(self, bb):
        board = np.unpackbits(np.array([bb], dtype=np.uint64).view(np.uint8))
        board = board.reshape(8, 8)[::-1]
        board = np.flip(board, axis=1)
        
        for row in board:
            print(' '.join(map(str, row)))



    
