from data.classes.Board.Move import Move
class Piece:
    def __init__(self, color: str, pos: tuple) -> None:
        self.color = color
        self.pos = pos

    def getValidMoves(self, board) -> list:
        output = []
        for move in self.getPossibleMoves(board):
            board.makeMove(move)
            if not board.isInCheck(self.color):
                output.append(move)
            board.unmakeMove(move)
        return output
    
    def columnShift(self, col: str, shift: int) -> str:
        return chr(ord(col)+shift)

    def isInBound(self, c: str, r: int) -> bool:
        return c in 'abcdefgh' and r in range(1, 9)
    
    def generateDirectionalMoves(self, board, directions: list, repeated=True) -> list:
        output = []
        for dc, dr in directions:
            curR = self.pos[1] + dr
            curC = self.columnShift(self.pos[0], dc)
            while(self.isInBound(curC, curR)): 
                piece = board.squares[(curC, curR)].occupying_piece
                if piece is None:
                    output.append(Move(board.squares[self.pos], board.squares[(curC, curR)]))
                elif piece.color != self.color:
                    output.append(Move(board.squares[self.pos], board.squares[(curC, curR)]))
                    break
                elif piece.color == self.color:
                    break
                
                if not repeated:
                    break
                
                curR = curR + dr
                curC = self.columnShift(curC, dc)
            
        return output