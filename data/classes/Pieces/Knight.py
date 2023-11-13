from data.classes.Piece import Piece
class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "N"


    def getPossibleMoves(self) -> list:
        return