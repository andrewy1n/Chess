from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':
    board.printBoard()

    for pos in board.squares:
        square = board.squares.get(pos)
        piece = square.occupying_piece
        if piece is not None:            
           print(piece.color + piece.notation + ': ' + str(piece.getPossibleMoves(board.squares)))
