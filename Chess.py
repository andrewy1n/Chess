class Chess:
    def __init__(self):
        self.chess_board = {
            ('a', 1): 'wr', ('b', 1): 'wn', ('c', 1): 'wb', ('d', 1): 'wq', ('e', 1): 'wk', ('f', 1): 'wb', ('g', 1): 'wn', ('h', 1): 'wr',
            ('a', 8): 'br', ('b', 8): 'bn', ('c', 8): 'bb', ('d', 8): 'bq', ('e', 8): 'bk', ('f', 8): 'bb', ('g', 8): 'bn', ('h', 8): 'br',  
        }
        for col in range(8):
            self.chess_board[(chr(97+col), 2)] = 'wp' #white pawns
            self.chess_board[(chr(97+col), 7)] = 'bp' #black pawns
        for row in range(3, 7):
            for col in range(8):
                self.chess_board[(chr(97+col), row)] = 'o' 
        self.moveCount = 0
    
    def move(self, start, end):
        self.chess_board[end] = self.board[start]
        self.board[start] = 'o'
    
    def printBoard(self):
        for row in range(8, 0, -1):
            for col in range(8):
                position = (chr(97 + col), row)
                print(self.chess_board.get(position, '  '), end=' ')
            print()
            
    def isLegal(self, start, end):
        if 
        #start and end are same color/or both are open
        if self.chess_board[start][0] == self.chess_board[end][0]:
            print('same color')
            return False
        
        #if starting spot is open
        if self.board[start][0] == 'o':
            print('start is open')
            return False

        #if both are the same
        if start == end:
            print('same position') 
            return False

        #check piece move legality
        startColor = self.chess_board[start][0]
        startPiece = self.chess_board[start][1]

        if startPiece == 'p':
            return self.pawnMoves(start, end, startColor)
        elif startPiece == 'r':
            return self.rookMoves(start, end, startColor)
        elif startPiece == 'b':
            return self.bishopMoves(start, end, startColor)
        elif startPiece == 'n':
            return self.knightMoves(start, end, startColor)
        elif startPiece == 'q':
            return self.queenMoves(start, end, startColor)
        elif startPiece == 'k':
            return self.kingMoves(start, end, startColor)
   
    def pawnMoves(self, start, end, color):
        legal_moves = set()
        #white and black different conditions
        if color == 'w':
            one_forward = start[0]+1
            twoSq = start[0]+2
        else:
            oneSq = start[0]-1
            twoSq = start[0]-2

        #pawn can take diagonals
        legal_moves.add((oneSq, start[1]+1)) if self.board[oneSq][start[1]+1][0] != color else legal_moves
        legal_moves.add((oneSq, start[1]-1)) if self.board[oneSq][start[1]-1][0] != color else legal_moves
        
        #pawn moves one space ahead
        legal_moves.add((oneSq, start[1])) if self.board[oneSq][start[1]][0] == 'o' else legal_moves

        #pawn can move two spaces if not moved yet
        legal_moves.add((twoSq, start[1])) if (start[0] == 1 and color == 'w' or start[0] == 6 and color == 'b') and self.board[oneSq][start[1]][0] == 'o' and self.board[twoSq][start[1]][0] == 'o' else moves

        return end in legal_moves
        
    def rookMoves(self, start, end, color):
        return True

    def bishopMoves(self, start, end, color):
        return True
    
    def knightMoves(self, start, end, color):
        return True

    def queenMoves(self, start, end, color):
        return self.bishopMoves and self.rookMoves
    
    def kingMoves(self, start, end, color):
        return True
        
    def startGame(self):
        print("Welcome to Chess")
        self.printBoard()
        while(not self.isWon()):
            #input for start and end
            while(True):
                print('Enter your start position: ')
                start = input()
                print('Enter your end position: ')
                end = input()

                start = tuple(map(int, start.split(', ')))
                end = tuple(map(int, end.split(', ')))
                
                print(self.chess_board[start])
                print(self.chess_board[end])

                if self.isLegal(start, end):
                    break
                else:
                    print("That move is not legal, please try again.")
            
            self.move(start, end)
            break

    def isWon(self):
        return False

        
        
