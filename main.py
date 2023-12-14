from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':
    board.squares[('f', 1)].occupying_piece = None
    board.squares[('g', 1)].occupying_piece = None
    board.squares[('d', 1)].occupying_piece = None
    board.squares[('c', 1)].occupying_piece = None
    board.squares[('b', 1)].occupying_piece = None
    board.printBoard()

    for pos in board.squares:
        square = board.squares.get(pos)
        piece = square.occupying_piece
        if piece is not None:            
           print(piece.color + piece.notation + ': ' + str(piece.getPossibleMoves(board.squares)))
