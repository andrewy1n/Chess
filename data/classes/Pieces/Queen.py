from data.classes.Piece import Piece
class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "Q"


    def getPossibleMoves(self) -> list:
        return