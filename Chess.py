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
        self.columns = 'abcdefgh'
        self.rows = '12345678'
        self.turn = 'w'
    
    def move(self, start, end):
        self.chess_board[end] = self.chess_board[start]
        self.chess_board[start] = 'o'
    
    def colShift(self, c, inc):
        return chr(ord(c)+inc)
    
    def printBoard(self):
        for row in range(8, 0, -1):
            for col in range(8):
                position = (chr(97 + col), row)
                print(self.chess_board.get(position, '  '), end=' ')
            print()
            
    def validInput(self, start, end):
        start, end = start.lower(), end.lower()
        #string must be length of 2
        if len(start) != len(end) != 2:
            return False
        #first char must be alpha in chess notation
        elif start[0] not in self.columns or end[0] not in self.columns:
            return False
        #second char must be num 1-8
        elif start[1] not in self.rows or end[1] not in self.rows:
            return False
        else:
            return True
    
    def isLegal(self, start, end, color):
        if self.chess_board[start][0] != color:
            print('wrong color')
            return False
        
        #start and end are same color/or both are open
        if self.chess_board[start][0] == self.chess_board[end][0]:
            print('same color')
            return False
        
        #if starting spot is open
        if self.chess_board[start][0] == 'o':
            print('start is open')
            return False

        #if both are the same
        if start == end:
            print('same position') 
            return False

        #check piece move legality
        startPiece = self.chess_board[start][1]

        legalMoves = set()
        if startPiece == 'p':
            legalMoves = self.pawnMoves(start, color)
        elif startPiece == 'r':
            legalMoves = self.rookMoves(start, color)
        elif startPiece == 'b':
            legalMoves = self.bishopMoves(start, color)
        elif startPiece == 'n':
            legalMoves = self.knightMoves(start, color)
        elif startPiece == 'q':
            legalMoves = self.queenMoves(start, color)
        elif startPiece == 'k':
            legalMoves = self.kingMoves(start, color)
        
        return end in legalMoves
    
    def pawnMoves(self, start, color):
        legal_moves = set()
        start_col, start_row = start[0], start[1]
        start_col_index = self.columns.index(start_col)
        #white and black different conditions
        if color == 'w':
            #if one space forward is open add to set
            
            if self.chess_board[(start_col, start_row+1)] == 'o':
                legal_moves.add((start_col, start_row+1))
                #given one space open, if two spaces is open and starts at 2, add to set
                if self.chess_board[(start_col, start_row+2)] == 'o' and start_row == 2: legal_moves.add((start_col, start_row+2)) 
            
            #diagonals are black pieces that can be taken
            if self.chess_board[(self.columns[start_col_index+1], start_row+1)][0] == 'b': legal_moves.add((self.columns[start_col_index+1], start_row+1))
            if self.chess_board[(self.columns[start_col_index-1], start_row+1)][0] == 'b': legal_moves.add((self.columns[start_col_index-1], start_row+1))
        
        else:
            #if one space forward is open add to set
            if self.chess_board[(start_col, start_row-1)] == 'o':
                legal_moves.add((start_col, start_row-1))
                #given one space open, if two spaces is open and starts at 2, add to set
                if self.chess_board[(start_col, start_row-2)] == 'o' and start_row == 7: legal_moves.add((start_col, start_row-2)) 
            
            #diagonals are white pieces that can be taken
            if self.chess_board[(self.columns[start_col_index-1], start_row-1)][0] == 'w': legal_moves.add((self.columns[start_col_index-1], start_row-1))
            if self.chess_board[(self.columns[start_col_index+1], start_row-1)][0] == 'w': legal_moves.add((self.columns[start_col_index+1], start_row-1))

        print(legal_moves)
        return legal_moves
        
    def rookMoves(self, start, color):
        legal_moves = set()
        left_distance = self.columns.index(start[0])
        right_distance = 8-left_distance
        down_distance = start[1]
        up_distance = 9-start[1]

        #add moves to the left
        for i in range(1, left_distance):
            col = self.colShift(start[0], -i)
            pos = (col, start[1])
            if self.chess_board[pos] == 'o':
                legal_moves.add(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.add(pos)
                break
            else:
                break
        
        #add moves to right
        for i in range(1, right_distance):
            col = self.colShift(start[0], i)
            pos = (col, start[1])
            if self.chess_board[pos] == 'o':
                legal_moves.add(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.add(pos)
                break
            else:
                break

        #add moves above
        for i in range(1, up_distance):
            row = start[1]+i
            pos = (start[0], row)
            if self.chess_board[pos] == 'o':
                legal_moves.add(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.add(pos)
                break
            else:
                break
        
        #add moves below
        for i in range(1, down_distance):
            row = start[1]-i
            pos = (start[0], row)
            if self.chess_board[pos] == 'o':
                legal_moves.add(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.add(pos)
                break
            else:
                break
        
        print(legal_moves)
        return legal_moves

    def bishopMoves(self, start, color):
        legal_moves = set()
        return legal_moves
    
    def knightMoves(self, start, color):
        legal_moves = set()
        position_pairs = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1)] #list of possible knight move distances
        for (x, y) in position_pairs:
            pos = (self.colShift(start[0], x), start[1]+y)
            if x > 0 and self.columns.index(start[0]) >= x: #if there's enough column space, positives only, or left
                if y > 0 and (8-start[1]) >= y: #if there's enough row space, positives only, or up
                    if self.chess_board[pos][0] != color: legal_moves.add(pos)
                elif y < 0 and start[1] >= -y: #if there's enough space on the bottom of the piece
                    if self.chess_board[pos][0] != color: legal_moves.add(pos)
            elif x < 0 and self.columns.index(start[0]) >= -x: #same thing for -x, or right of piece
                if y > 0 and (8-start[1]) >= y:
                    if self.chess_board[pos][0] != color: legal_moves.add(pos)
                elif y < 0 and start[1] >= -y:
                    if self.chess_board[pos][0] != color: legal_moves.add(pos)
        
        print(legal_moves)
        return legal_moves

    def queenMoves(self, start, color):
        return self.bishopMoves(start, color) + self.rookMoves(start, color)
    
    def kingMoves(self, start, end, color):
        return True
        
    def startGame(self):
        print("Welcome to Chess")
        self.printBoard()
        while(not self.isWon()):
            while(True):
                while(True):
                    #check for valid inputs
                    print('Enter your start position: ')
                    start_input = input()
                    print('Enter your end position: ')
                    end_input = input()
                    if self.validInput(start_input, end_input):
                        break
                #check for legal move
                start = tuple((start_input[0].lower(), int(start_input[1])))
                end = tuple((end_input[0].lower(), int(end_input[1])))
                
                print(self.chess_board[start])
                print(self.chess_board[end])

                if self.isLegal(start, end, self.turn):
                    break
                else:
                    print("That move is not legal, please try again.")
            
            self.move(start, end)
            self.printBoard()
            if self.turn == 'w':
                self.turn = 'b'
            else:
                self.turn = 'w' 
        
    def isWon(self):
        return False

        
        
