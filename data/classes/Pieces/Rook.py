from data.classes.Piece import Piece
class Rook(Piece):
    def __init__(self, color: str, pos: tuple) -> None:
        super().__init__(color, pos)
        self.notation = "R"
        self.has_moved = False #for castling
        self.black_piece_image_path  = 'data/images/rook-b.svg'
        self.white_piece_image_path  = 'data/images/rook-w.svg'


    def getPossibleMoves(self, squares, moves) -> list:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        return super().generateMoves(squares, directions)