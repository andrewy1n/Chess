from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':
    board.squares[('e', 2)].occupying_piece.move(('e', 6), board)
    board.printBoard()

    for square in board.squares.values():
        piece = square.occupying_piece
        if piece is not None:
            print(piece.color + piece.notation)
            print(piece.pos)
            print([(sq.c, sq.r) for sq in piece.getPossibleMoves(board)])
