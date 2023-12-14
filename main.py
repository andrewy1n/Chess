from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':
    board.printBoard()

    for square in board.squares.values():
        piece = square.occupying_piece
        if piece is not None:
            print(piece.color + piece.notation)
            print([(sq.c, sq.r) for sq in piece.getPossibleMoves(board)])
