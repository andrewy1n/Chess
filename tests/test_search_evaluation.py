import unittest
from data.classes.Board.Board import Board
from data.classes.Evaluation import Evaluation
from data.classes.Search import Search  

class BoardTests(unittest.TestCase):
    def test_evaluation(self):
        board = Board()
        print(Evaluation.evaluate(board))
        self.assertEqual(0, Evaluation.evaluate(board))
    
if __name__ == '__main__':
    unittest.main()