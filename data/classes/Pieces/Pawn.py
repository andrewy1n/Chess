from data.classes.Piece import Piece
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "P"

    def getPossibleMoves(self) -> list:
        return