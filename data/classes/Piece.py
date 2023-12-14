from copy import deepcopy
class Piece:
    def __init__(self, color: str, pos: tuple) -> None:
        self.color = color
        self.pos = pos
    
    def move(self, to_pos: tuple, board) -> None:
        prev_square = board.squares[self.pos]
        prev_square.occupying_piece = None
        self.pos = to_pos
        board.squares[to_pos].occupying_piece = self

        board.moves.append([self.color, prev_square, board.squares[to_pos], deepcopy(board.squares)])

    def getMoves(self, board: dict) -> list:
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
    
    def getValidMoves(self, board: dict) -> list:
        output = []
        for square in self.getMoves(board):
            if not board.isInCheck(self.color, board_change = [self.pos, square.pos]):
                output.append(square)
        return output
    
    def columnShift(self, col: str, shift: int) -> str:
        return chr(ord(col)+shift)