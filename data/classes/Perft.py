from data.classes.Board.Board import Board

class Perft:
    def __init__(self, FEN_string=None):
        self.board = Board(FEN_string=FEN_string) if FEN_string is not None else Board()

    def perft(self, depth):
        print()
        return self.perft_alg(depth, depth)

    def perft_alg(self, depth, current_depth):
        nodes = 0
        if current_depth == 0:
            return 1
        else:
            moves = self.board.piece_list.getAllValidMoves(self.board.turn, self.board)
            for m in moves:
                self.board.makeMove(m)
                node_for_move = self.perft_alg(depth, current_depth - 1)
                nodes += node_for_move
                if current_depth == depth:
                    print(f"{m.start_pos} {m.target_pos}: {node_for_move}")
                self.board.unmakeMove(m)
        return nodes

