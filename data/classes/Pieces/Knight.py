from data.classes.Piece import Piece
class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "N"


    def getPossibleMoves(self, board: dict) -> list:
        output = []
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            if ((curR in range(1, 9))
                and curC in 'abcdefgh'
                and (board[(curC, curR)].occupying_piece is None
                or board[(curC, curR)].occupying_piece.color != self.color)):
                output.append((curC, curR))
            
        return output