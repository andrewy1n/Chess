from data.classes.Piece import Piece
class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "P"

    def getPossibleMoves(self, board: dict) -> list:
        output = []
        cm = 1 #color positional modifier
        
        #white and black different conditions
        if self.color == 'b':
            cm = -1
        
        #if one space forward is open add to set            
        if board[(self.pos[0], self.pos[1]+1*cm)].occupying_piece is None:
            output.append((self.pos[0], self.pos[1]+1*cm))
            #given one space open, if two spaces is open and starts at 2, add to set
            if(board[(self.pos[0], self.pos[1]+2*cm)].occupying_piece is None 
            and (self.pos[1] == 2 and self.color == 'w')
            or (self.pos[1] == 7 and self.color == 'b')): 
                output.append((self.pos[0], self.pos[1]+2*cm)) 
        
        #diagonals are black pieces that can be taken
        if (self.pos[0] < 'h'
            and board[(super().columnShift(self.pos[0], 1), self.pos[1]+1*cm)].occupying_piece is not None 
            and board[(super().columnShift(self.pos[0], 1), self.pos[1]+1*cm)].occupying_piece.color != self.color): 
            output.append((super().columnShift(self.pos[0], 1), self.pos[1]+1*cm))
        
        if (self.pos[0] > 'a'
            and board[(super().columnShift(self.pos[0], -1), self.pos[1]+1*cm)].occupying_piece is not None
            and board[(super().columnShift(self.pos[0], -1), self.pos[1]+1*cm)].occupying_piece.color != self.color): 
            output.append((super().columnShift(self.pos[0], -1*cm), self.pos[1]+1*cm))

        return output