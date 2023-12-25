import unittest
from ..classes.Board import Board

def MoveGenerationTest(depth: int, board) -> int:   
        moves = board.piece_list.getAllValidMoves(board.turn, board)     
        num_positions = 0

        if depth == 1:
            return len(moves)

        for move in moves:
            board.makeMove(move)
            num_positions += MoveGenerationTest(depth-1, board)
            board.unmakeMove(move)
        
        return num_positions

class TestMoveGeneration(unittest.TestCase):
    """
    def test_move_generation_pos_5_board_1ply(self):
        board = Board(FEN_string="rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
        self.assertEqual(MoveGenerationTest(1, board), 44)

    def test_move_generation_pos_5_board_2ply(self):
        board = Board(FEN_string="rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
        self.assertEqual(MoveGenerationTest(2, board), 1486)
    
    """
    def test_move_generation_start_board_1ply(self):
        board = Board()
        self.assertEqual(MoveGenerationTest(1, board), 20)
    
    def test_move_generation_start_board_2ply(self):
        board = Board()
        self.assertEqual(MoveGenerationTest(2, board), 400)
    
    def test_move_generation_start_board_3ply(self):
        board = Board()
        self.assertEqual(MoveGenerationTest(3, board), 8902)
    
    def test_move_generation_start_board_4ply(self):
        board = Board()
        self.assertEqual(MoveGenerationTest(4, board), 197281)
    
    """
    def test_move_generation_start_board_5ply(self):
        self.assertEqual(MoveGenerationTest(5, Board()), 4865609)
    
    def test_move_generation_start_board_6ply(self):
        self.assertEqual(MoveGenerationTest(6, Board()), 119060324)
    """

if __name__ == '__main__':
    unittest.main()