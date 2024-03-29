from data.classes.Board.Piece import Piece

class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "B"
        self.black_piece_image_path  = 'data/images/bishop-b.png'
        self.white_piece_image_path  = 'data/images/bishop-w.png'

    def getPossibleMoves(self, board) -> list:
        return super().generateDirectionalMoves(board, board.ordinals)

    def getAttackingMoves(self, board):
        return self.getPossibleMoves(board)