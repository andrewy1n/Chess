from data.classes.Piece import Piece
class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "B"
        self.black_piece_image_path  = 'data/images/bishop-b.svg'
        self.white_piece_image_path  = 'data/images/bishop-w.svg'

    def getPossibleMoves(self, squares, moves) -> list:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        return super().generateMoves(squares, directions)