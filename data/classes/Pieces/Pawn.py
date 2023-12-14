from data.classes.Piece import Piece
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "P"

    def getPossibleMoves(self, board) -> list:
        output = []
        cm = 1 #color positional modifier
        
        #white and black different conditions
        if self.color == 'b':
            cm = -1
        
        #if one space forward is open add to set            
        if board.squares[(self.pos[0], self.pos[1]+1*cm)].occupying_piece is None:
            output.append(board.squares[(self.pos[0], self.pos[1]+1*cm)])
            #given one space open, if two spaces is open and starts at 2, add to set
            if(board.squares[(self.pos[0], self.pos[1]+2*cm)].occupying_piece is None 
            and (self.pos[1] == 2 and self.color == 'w')
            or (self.pos[1] == 7 and self.color == 'b')): 
                output.append(board.squares[(self.pos[0], self.pos[1]+2*cm)]) 
        
        #diagonals are black pieces that can be taken
        if (ord(self.pos[0]) < ord('h') #right
            and board.squares[(super().columnShift(self.pos[0], 1), self.pos[1]+1*cm)].occupying_piece is not None 
            and board.squares[(super().columnShift(self.pos[0], 1), self.pos[1]+1*cm)].occupying_piece.color != self.color): 
            output.append(board.squares[(super().columnShift(self.pos[0], 1), self.pos[1]+1*cm)])
        
        if (ord(self.pos[0]) > ord('a') #left
            and board.squares[(super().columnShift(self.pos[0], -1), self.pos[1]+1*cm)].occupying_piece is not None
            and board.squares[(super().columnShift(self.pos[0], -1), self.pos[1]+1*cm)].occupying_piece.color != self.color): 
            output.append(board.squares[(super().columnShift(self.pos[0], -1), self.pos[1]+1*cm)])
        
        #en passant
        pawn_row = 5
        if self.color != 'w':
            pawn_row = 4
        
        if(self.pos[1] == pawn_row and len(board.moves) > 0):
            prev_piece = board.moves[-1][2].occupying_piece
            pawn_dist = ord(prev_piece.pos[0]) - ord(self.pos[0])

            if(prev_piece.notation == 'P'
                and prev_piece.pos[1] == pawn_row
                and abs(pawn_dist) == 1):
                output.append(board.squares[(super().columnShift(self.pos[0], pawn_dist), self.pos[1]+1*cm)])

        return output