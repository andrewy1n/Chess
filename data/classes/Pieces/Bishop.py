from data.classes.Piece import Piece
class Bishop(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "B"


    def getPossibleMoves(self) -> list:
        return