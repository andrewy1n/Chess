import unittest
from data.classes.Perft import Perft

class TestMoveGeneration(unittest.TestCase):
    
    def test_move_generation_pos_5_board_1ply(self):
        perft = Perft("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        self.assertEqual(perft.perft(1), 44)
        
    def test_move_generation_pos_5_board_2ply(self):
        perft = Perft("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        self.assertEqual(perft.perft(2), 1486)
    
    def test_move_generation_start_board_1ply(self):
        perft = Perft()
        self.assertEqual(perft.perft(1), 20)
    
    def test_move_generation_start_board_2ply(self):
        perft = Perft()
        self.assertEqual(perft.perft(2), 400)
    
    def test_move_generation_start_board_3ply(self):
        perft = Perft()
        self.assertEqual(perft.perft(3), 8902)

    def test_move_generation_start_board_4ply(self):
        perft = Perft()
        self.assertEqual(perft.perft(4), 197281)
    
    """
    def test_move_generation_start_board_6ply(self):
        self.assertEqual(MoveGenerationTest(6, Board()), 119060324)
    """

if __name__ == '__main__':
    unittest.main()