class Piece:
    def __init__(self, color, pos) -> None:
        self.color = color
        self.pos = pos
    
    def move(self, square, board) -> None:
        prev_square = board.squares[self.pos]
        self.pos = (square.c, square.r)
        prev_square.occupying_piece = None
        square.occupying_piece = self

    def getMoves(self, board) -> list:
        output = []
        for square in self.getPossibleMoves(board):
            if square.occupying_piece is not None:
                if square.occupying_piece.color == self.color:
                    break
                else:
                    output.append(square)
                    break
            else:
                output.append(square)
        return output
    
    def getValidMoves(self, board) -> list:
        output = []
        for square in self.getMoves(board):
            if not board.isInCheck(self.color, board_change = [self.pos, square.pos]):
                output.append(square)
        return output
    
    def columnShift(self, col: str, shift: int) -> str:
        return chr(ord(col)+shift)