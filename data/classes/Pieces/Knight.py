from data.classes.Piece import Piece
class Knight(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "N"
        self.black_piece_image_path  = 'data/images/knight-b.svg'
        self.white_piece_image_path  = 'data/images/knight-w.svg'


    def getPossibleMoves(self, squares, moves) -> list:
        output = []
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            if ((super().isInBound(curC, curR)) and 
                (squares[(curC, curR)].occupying_piece is None or 
                 squares[(curC, curR)].occupying_piece.color != self.color)):
                output.append(squares[(curC, curR)])
            
        return output