from data.classes.Piece import Piece
class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"
        self.has_moved = False #for castling
        self.black_piece_image_path  = 'data/images/king-b.svg'
        self.white_piece_image_path  = 'data/images/king-w.svg'

    def getPossibleMoves(self, squares, moves) -> list:
        output = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            
            if (curR in range(1, 9)
                and curC in 'abcdefgh' 
                and (squares[(curC, curR)].occupying_piece is None
                or  squares[(curC, curR)].occupying_piece.color != self.color)): #append attacking squares
                output.append(squares[(curC, curR)])
        
        
        if(not self.has_moved):
            rookRow = self.pos[1]

            #king side castling
            if (squares[('h', rookRow)].occupying_piece is not None and
                squares[('h', rookRow)].occupying_piece.notation == 'R'
                and not squares[('h', rookRow)].occupying_piece.has_moved
                and squares[('f', rookRow)].occupying_piece is None
                and squares[('g', rookRow)].occupying_piece is None):
                output.append(squares[('g', rookRow)])
            
            #queen side castling
            if (squares[('a', rookRow)].occupying_piece is not None and
                squares[('a', rookRow)].occupying_piece.notation == 'R'
                and not squares[('a', rookRow)].occupying_piece.has_moved
                and squares[('c', rookRow)].occupying_piece is None
                and squares[('b', rookRow)].occupying_piece is None
                and squares[('d', rookRow)].occupying_piece is None):
                output.append(squares[('c', rookRow)]) 
        
        return output
    