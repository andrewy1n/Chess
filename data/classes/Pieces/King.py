from data.classes.Piece import Piece
class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"

    def getPossibleMoves(self) -> list:
        return
    