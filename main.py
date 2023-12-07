from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':

    for pos in board.squares:
        square = board.squares.get(pos)
        piece = square.occupying_piece
        print(pos, piece, square)
        if piece is not None and piece.notation == "P":            
           print(piece.getPossibleMoves(board.squares))
