from data.classes.Piece import Piece
class Rook(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "R"


    def getPossibleMoves(self) -> list:
        return