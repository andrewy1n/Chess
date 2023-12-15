from data.classes.Board import Board

board = Board()
turn = 'w'
running = True

def validInput(startInput, endInput) -> bool:
    if(len(startInput) != 2 or
       startInput[0] not in 'abcdefgh' or
       startInput[1] not in '12345678'): #basic validity coordinates must be within the chess board
        return False

    elif(len(endInput) != 2 or
       endInput[0] not in 'abcdefgh' or
       endInput[1] not in '12345678'):
        return False

    startPos = (startInput[0], int(startInput[1]))
    endPos = (endInput[0], int(endInput[1]))
    
    if(board.squares[startPos].occupying_piece is None or
       board.squares[startPos].occupying_piece.color != turn or
       endPos == startPos): #start position validation
        return False
    
    piece = board.squares[startPos].occupying_piece

    if(board.squares[endPos] not in piece.getValidMoves(board)):
        return False
    
    return True

def testPrintAllValidMoves():
    for square in board.squares.values():
        piece = square.occupying_piece
        if piece is not None and piece.color == turn:
            print(str(piece.pos) + ' ' + piece.color + piece.notation)
            print([(sq.c, sq.r) for sq in piece.getValidMoves(board)])

if __name__ == '__main__':
    while running:
        board.printBoard()
        testPrintAllValidMoves()
        if turn == 'w':
            print("White to Move")
        else:
            print("Black to Move")
        
        while(True):
            startInput = input("Enter Start Position: ")
            endInput = input("Enter End Position: ")
            
            if validInput(startInput, endInput):
                break
            
            print("Invalid Input")
        
        startPos = (startInput[0], int(startInput[1]))
        endPos = (endInput[0], int(endInput[1]))
        piece_selected = board.squares[startPos].occupying_piece
        
        board = piece_selected.move(endPos, board, permanent = True)
        
        board.moves.append([turn, board.squares[endPos], board.squares[endPos]])

        if board.isCheckMate(turn):
            if turn == 'w':
                print("White Wins!")
            else:
                print("Black Wins!")
            running = False
        elif board.isStaleMate():
            print("Stalemate")
            running = False
        
        turn = 'b' if turn == 'w' else 'w'