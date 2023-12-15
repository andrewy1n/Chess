from data.classes.Piece import Piece
class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"
        self.has_moved = False #for castling

    def getPossibleMoves(self, board) -> list:
        output = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            
            if (curR in range(1, 9)
                and curC in 'abcdefgh' 
                and (board.squares[(curC, curR)].occupying_piece is None
                or board.squares[(curC, curR)].occupying_piece.color != self.color)): #append attacking squares
                output.append(board.squares[(curC, curR)])
        
        
        if(not self.has_moved):
            rookRow = self.pos[1]

            #king side castling
            if (board.squares[('h', rookRow)].occupying_piece.notation == 'R'
                and not board.squares[('h', rookRow)].occupying_piece.has_moved
                and board.squares[('f', rookRow)].occupying_piece is None
                and board.squares[('g', rookRow)].occupying_piece is None):
                output.append(board.squares[('g', rookRow)])
            
            #queen side castling
            if (board.squares[('a', rookRow)].occupying_piece.notation == 'R'
                and not board.squares[('a', rookRow)].occupying_piece.has_moved
                and board.squares[('c', rookRow)].occupying_piece is None
                and board.squares[('b', rookRow)].occupying_piece is None
                and board.squares[('d', rookRow)].occupying_piece is None):
                output.append(board.squares[('c', rookRow)]) 
        
        return output
    