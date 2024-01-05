from data.classes.Board.Piece import Piece

class Rook(Piece):
    def __init__(self, color: str, pos: tuple) -> None:
        super().__init__(color, pos)
        self.notation = "R"
        self.black_piece_image_path  = 'data/images/rook-b.png'
        self.white_piece_image_path  = 'data/images/rook-w.png'

    def getPossibleMoves(self, board) -> list:
        return super().generateDirectionalMoves(board, board.cardinals)
    
    def getAttackingMoves(self, board):
        return self.getPossibleMoves(board)