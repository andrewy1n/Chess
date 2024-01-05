from data.classes.Board.Piece import Piece

class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "Q"
        self.black_piece_image_path  = 'data/images/queen-b.png'
        self.white_piece_image_path  = 'data/images/queen-w.png'

    def getPossibleMoves(self, board) -> list:
        return super().generateDirectionalMoves(board, board.cardinals + board.ordinals)
    
    def getAttackingMoves(self, board):
        return self.getPossibleMoves(board)