from copy import deepcopy
class Piece:
    def __init__(self, color: str, pos: tuple) -> None:
        self.color = color
        self.pos = pos
    
    def move(self, to_pos: tuple, squares: dict, permanent = False):
        #if King castles
        dummy_squares = deepcopy(squares)
        
        if self.notation == 'K' and abs(ord(to_pos[0])-ord(self.pos[0])) == 2:
            if(to_pos[0] == 'g' and to_pos[1] == self.pos[1]): #King side
                king_side_rook = dummy_squares[('h', self.pos[1])].occupying_piece
                dummy_squares[('h', self.pos[1])].occupying_piece = None
                dummy_squares[('f', self.pos[1])].occupying_piece = king_side_rook
            else: #Queen side
                queen_side_rook = dummy_squares[('a', self.pos[1])].occupying_piece
                dummy_squares[('a', self.pos[1])].occupying_piece = None
                dummy_squares[('d', self.pos[1])].occupying_piece = queen_side_rook
        
        if(self.notation == 'P' 
            and ord(self.pos[0]) - ord(to_pos[0]) != 0 #en passant
            and dummy_squares[to_pos].occupying_piece is None):
            dummy_squares[(to_pos[0], self.pos[1])].occupying_piece = None

        prev_square = dummy_squares[self.pos]
        prev_square.occupying_piece = None
        dummy_squares[to_pos].occupying_piece = self

        if(self.notation == 'P' and (to_pos[1] == 1 or to_pos[1] == 8)): #promotion
            from data.classes.Pieces.Queen import Queen
            dummy_squares[(self.pos)].occupying_piece = Queen(self.color, self.pos)
        
        if permanent:
            self.pos = to_pos
            if (self.notation == 'K' or self.notation == 'R'):
                self.has_moved = True
            
        return dummy_squares

    def getValidMoves(self, board) -> list:
        output = []
        for square in self.getPossibleMoves(board.squares, board.moves):
            if not board.isInCheck(self.color, self.move((square.c, square.r), board.squares)):
                output.append(square)
        return output
    
    def columnShift(self, col: str, shift: int) -> str:
        return chr(ord(col)+shift)