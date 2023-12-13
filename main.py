from data.classes.Board import Board

board = Board()

def validInput(inputPos) -> bool:
    return

if __name__ == '__main__':
    sq = board.squares[('d', 4)]
    board.squares[('d', 2)].occupying_piece.move(sq, board.squares)
    board.squares[('b', 2)].occupying_piece.move(board.squares[('b', 4)], board.squares)
    board.squares[('b', 7)].occupying_piece.move(board.squares[('b', 5)], board.squares)
    board.squares[('d', 7)].occupying_piece.move(board.squares[('d', 5)], board.squares)
    board.printBoard()

    for pos in board.squares:
        square = board.squares.get(pos)
        piece = square.occupying_piece
        if piece is not None and piece.notation == "B":            
           print(piece.getPossibleMoves(board.squares))
