import random

class RandomBot:
    def __init__(self) -> None:
        pass

    def getMove(self, board):
        all_moves = board.piece_list.getAllValidMoves(board.turn, board)
        rand_index = random.randint(0, len(all_moves)-1)

        return all_moves[rand_index]