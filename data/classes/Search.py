from data.classes.Evaluation import Evaluation
from data.classes.Board.Board import Board
import heapq
import math

class Search:
    @staticmethod
    def search(depth, alpha, beta, board: Board):
        if depth == 0:
            return Evaluation.evaluate(board), None  # Return evaluation and best move
        
        moves = board.piece_list.getOrderedMoves(board.turn, board)

        if len(moves) == 0:
            if board.isInCheck(board.turn):
                return -math.inf, None
            return 0, None

        best_move = None
        for score, move in moves:
            board.makeMove(move)
            evaluation, _ = Search.search(depth - 1, -beta, -alpha, board)
            evaluation = -evaluation
            if evaluation >= beta:
                board.unmakeMove(move)
                return beta, move
            
            if evaluation > alpha:
                alpha = evaluation
                best_move = move

            board.unmakeMove(move)
        
        return alpha, best_move

        