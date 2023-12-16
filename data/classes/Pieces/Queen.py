from data.classes.Piece import Piece
from data.classes.Pieces.Rook import Rook
from data.classes.Pieces.Bishop import Bishop
class Queen(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "Q"
        self.black_piece_image_path  = 'data/images/queen-b.svg'
        self.white_piece_image_path  = 'data/images/queen-w.svg'


    def getPossibleMoves(self, squares, moves) -> list:
        output = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            while((curR in range(1, 9)) #append open squares
                and curC in 'abcdefgh'
                and squares[(curC, curR)].occupying_piece is None):
                output.append(squares[(curC, curR)])
                curR = curR + dr
                curC = super().columnShift(curC, dc)
            
            if (curR in range(1, 9)
                and curC in 'abcdefgh' 
                and squares[(curC, curR)].occupying_piece.color != self.color): #append attacking squares
                output.append(squares[(curC, curR)])

        return output