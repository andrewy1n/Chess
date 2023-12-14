from data.classes.Piece import Piece
class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"
        self.has_moved = False #for castling

    def getPossibleMoves(self, board: dict) -> list:
        output = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = super().columnShift(self.pos[0], dc)
            
            if (curR in range(1, 9)
                and curC in 'abcdefgh' 
                and (board[(curC, curR)].occupying_piece is None
                or board[(curC, curR)].occupying_piece.color != self.color)): #append attacking squares
                output.append((curC, curR))
        
        
        if(not self.has_moved):
            rookRow = self.pos[1]
            
            #king side castling
            if (board[('h', rookRow)].occupying_piece.notation == 'R'
                and not board[('h', rookRow)].occupying_piece.has_moved
                and ('f', rookRow) in output
                and board[('g', rookRow)].occupying_piece is None):
                output.append(('g', rookRow))
            
            #queen side castling
            if (board[('a', rookRow)].occupying_piece.notation == 'R'
                and not board[('a', rookRow)].occupying_piece.has_moved
                and ('d', rookRow) in output
                and board[('c', rookRow)].occupying_piece is None
                and board[('b', rookRow)].occupying_piece is None):
                output.append(('c', rookRow)) 
        
        return output
    