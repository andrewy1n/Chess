import unittest
from data.classes.Board.Board import Board  

class BoardTests(unittest.TestCase):
    def test_king_moves(self):
       board = Board()
       
       white_king = board.squares[board.white_king_pos].occupying_piece
       self.assertEqual(white_king.getValidMoves(board), [])
    
    def test_pawn_moves(self):
        board = Board()

        e2_pawn = board.squares[('e', 2)].occupying_piece
        pawn_moves = e2_pawn.getValidMoves(board)

        move_positions = [move.target_pos for move in pawn_moves]
        self.assertEqual(move_positions, [('e', 3), ('e', 4)])

        board.makeMove(pawn_moves[1]) #Pawn e2 -> e4

        d7_pawn = board.squares['d', 7].occupying_piece
        pawn_moves = d7_pawn.getValidMoves(board)
            
        board.makeMove(pawn_moves[1]) #Pawn d7 -> d5

        e4_pawn = board.squares[('e', 4)].occupying_piece
        pawn_moves = e4_pawn.getValidMoves(board)
        move_positions = [move.target_pos for move in pawn_moves]
        self.assertEqual(move_positions, [('e', 5), ('d', 5)])

        board.makeMove(pawn_moves[1]) #Pawn e4 captures pawn d5
        
        e7_pawn = board.squares[('e', 7)].occupying_piece
        pawn_moves = e7_pawn.getValidMoves(board)
        
        board.makeMove(pawn_moves[1]) #Pawn e7 -> e5

        d5_pawn = board.squares[('d', 5)].occupying_piece           
        pawn_moves = d5_pawn.getValidMoves(board)
        move_positions = [move.target_pos for move in pawn_moves]
        
        self.assertEqual(move_positions, [('d', 6), ('e', 6)]) #En Passant
        board.makeMove(pawn_moves[1])
    
    def test_pawn_promotions(self):
        board = Board(FEN_string="rnbqkbnr/pPpppppp/8/8/8/8/PPPPPPPP/R3K2R w kqKQ - 0 1")
        promoting_pawn = board.squares[('b', 7)].occupying_piece
        moves = promoting_pawn.getValidMoves(board)

        self.assertEqual(moves[0].is_promotion, True)
        self.assertEqual(len(moves), 8)

    def test_castling_moves(self):
        board = Board(FEN_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w kqKQ - 0 1")
        white_king = board.squares[board.white_king_pos].occupying_piece
        moves = [move.target_pos for move in white_king.getValidMoves(board)]
        self.assertEqual(('g', 1) in moves, True)
        self.assertEqual(('c', 1) in moves, True)

    def test_in_check(self):
        board = Board(FEN_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK1qR w kqKQ - 0 1")
        self.assertEqual(board.isInCheck(board.turn), True)
    
    def test_checkmate(self):
        board = Board(FEN_string="rnbqkbnr/pppp1Qpp/8/4N3/8/8/PPPPPPPP/RNB1KB1R b kqKQ - 0 1")
        board.turn = 'b'
        self.assertEqual(board.isCheckMate(), True)
    
    def test_stalemate(self):
        board = Board(FEN_string="k7/1R1RN3/p3p3/P3P2p/1PP4P/3K1PP1/8/8 b - - 0 1")
        board.turn = 'b'
        self.assertEqual(board.isStaleMate(), True)
    
if __name__ == '__main__':
    unittest.main()