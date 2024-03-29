from data.classes.Board.Piece import Piece
class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "N"
        self.black_piece_image_path  = 'data/images/knight-b.png'
        self.white_piece_image_path  = 'data/images/knight-w.png'


    def getPossibleMoves(self, board) -> list:
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
            
        return super().generateDirectionalMoves(board, directions, repeated=False)
    
    def getAttackingMoves(self, board):
        return self.getPossibleMoves(board)