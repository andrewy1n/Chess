from data.classes.Piece import Piece
class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "Q"
        self.black_piece_image_path  = 'data/images/queen-b.svg'
        self.white_piece_image_path  = 'data/images/queen-w.svg'


    def getPossibleMoves(self, squares, moves) -> list:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        return super().generateMoves(squares, directions)