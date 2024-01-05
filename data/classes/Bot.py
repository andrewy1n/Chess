from data.classes.Search import Search
from data.classes.OpeningBook import OpeningBook
from data.classes.Board.Move import Move
import math

class Bot:
    def __init__(self) -> None:
        self.book = OpeningBook("data/resources/Book.txt")

    def getBestMove(self, board):
        #If position has book move, play it
        if self.book.hasMove(board):
            move = self.book.getMove(board)
            start_pos = (move[0], int(move[1]))
            end_pos = (move[2], int(move[3]))
            return 0, Move(board.squares[start_pos], board.squares[end_pos])
        
        #else, search and evaluate
        best_evaluation, best_move = Search.search(3, -math.inf, math.inf, board)
        return best_evaluation, best_move
