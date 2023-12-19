from copy import deepcopy
class Piece:
    def __init__(self, color: str, pos: tuple) -> None:
        self.color = color
        self.pos = pos
    
    def move(self, to_pos: tuple, board, permanent = False) -> dict:
        squares = deepcopy(board.squares)
        #if King castles
        if(self.notation == 'K' and abs(ord(to_pos[0])-ord(self.pos[0])) == 2):
            if board.isInCheck(self.color, squares):
                return squares
            
            elif(to_pos[0] == 'g' and to_pos[1] == self.pos[1]): #King side
                if board.isAttacked(self.color, ('f', self.pos[1]), squares):
                    return self.move(('f', self.pos[1]), board)
                
                king_side_rook = squares[('h', self.pos[1])].occupying_piece
                squares[('h', self.pos[1])].occupying_piece = None
                squares[('f', self.pos[1])].occupying_piece = king_side_rook
                
                if permanent:
                    king_side_rook.pos = ('f', self.pos[1])
            
            elif(to_pos[0] == 'c' and to_pos[1] == self.pos[1]): #Queen side
                if board.isAttacked(self.color, ('d', self.pos[1]), squares):
                    return self.move(('d', self.pos[1]), board)
                
                queen_side_rook = squares[('a', self.pos[1])].occupying_piece
                squares[('a', self.pos[1])].occupying_piece = None
                squares[('d', self.pos[1])].occupying_piece = queen_side_rook

                if permanent:
                    queen_side_rook.pos = ('d', self.pos[1])
        
        if(self.notation == 'P' 
            and ord(self.pos[0]) - ord(to_pos[0]) != 0 #en passant
            and squares[to_pos].occupying_piece is None):
            squares[(to_pos[0], self.pos[1])].occupying_piece = None

        prev_square = squares[self.pos]
        prev_square.occupying_piece = None

        if(self.notation == 'P' and (to_pos[1] == 1 or to_pos[1] == 8)): #promotion
            from data.classes.Pieces.Queen import Queen
            squares[to_pos].occupying_piece = Queen(self.color, to_pos)
        else:
            squares[to_pos].occupying_piece = self
        
        if permanent:
            self.pos = to_pos
            if (self.notation == 'K' or self.notation == 'R'):
                self.has_moved = True
        
        return squares

    def getValidMoves(self, board) -> list:
        output = []
        for square in self.getPossibleMoves(board.squares, board.moves):
            new_board_state = self.move((square.c, square.r), board)
            if not board.isInCheck(self.color, new_board_state):
                output.append(square)
        return output
    
    def columnShift(self, col: str, shift: int) -> str:
        return chr(ord(col)+shift)

    def isInBound(self, c: str, r: int) -> bool:
        return c in 'abcdefgh' and r in range(1, 9)
    
    def generateMoves(self, squares: dict, directions: list) -> list:
        output = []
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = self.columnShift(self.pos[0], dc)
            while(self.isInBound(curC, curR)):
                piece = squares.get((curC, curR)).occupying_piece
                if piece is None:
                    output.append(squares[(curC, curR)])
                elif piece.color != self.color:
                    output.append(squares[(curC, curR)])
                    break
                else:
                    break
                
                curR = curR + dr
                curC = self.columnShift(curC, dc)
            
        return output