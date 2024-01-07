from data.classes.Board.Board import Board
from data.classes.Bitboard import Bitboard

board = Board()
w_bb = Bitboard(board.piece_list.white_pieces)
w_bb.initializeBB()