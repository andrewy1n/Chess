#old class
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
        self.white_king_pos = ('e', 1)
        self.black_king_pos = ('e', 8)
    
    def move(self, start, end, board):
        if self.chess_board[start][0] == self.turn:
            if self.chess_board[start][1] == 'k':
                if self.turn == 'w':
                    self.white_king_pos = end
                else:
                    self.black_king_pos = end
        board[end] = board[start]
        board[start] = 'o'
    
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
        if(len(start) != len(end) != 2      
        #first char must be alpha in chess notation
        or start[0] not in self.columns or end[0] not in self.columns
        #second char must be num 1-8
        or start[1] not in self.rows or end[1] not in self.rows):
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
        
        pieces, moves = self.getAllMoves(color)
        return end in self.getValidMoves(moves, pieces)

    def legalMoves(self, start, color):
        #check piece move legality
        startPiece = self.chess_board[start][1]

        legal_moves = []
        if startPiece == 'p':
            legal_moves = self.pawnMoves(start, color)
        elif startPiece == 'r':
            legal_moves = self.rookMoves(start, color)
        elif startPiece == 'b':
            legal_moves = self.bishopMoves(start, color)
        elif startPiece == 'n':
            legal_moves = self.knightMoves(start, color)
        elif startPiece == 'q':
            legal_moves = self.queenMoves(start, color)
        elif startPiece == 'k':
            legal_moves = self.kingMoves(start, color)
        

        return legal_moves
    
    def pawnMoves(self, start, color):
        legal_moves = []
        start_col, start_row = start[0], start[1]
        start_col_index = self.columns.index(start_col)
        #white and black different conditions
        if color == 'w':
            #if one space forward is open add to set            
            if self.chess_board[(start_col, start_row+1)] == 'o':
                legal_moves.append((start_col, start_row+1))
                #given one space open, if two spaces is open and starts at 2, add to set
                if self.chess_board[(start_col, start_row+2)] == 'o' and start_row == 2: legal_moves.append((start_col, start_row+2)) 
            
            #diagonals are black pieces that can be taken
            if start_col_index < 7:
                if self.chess_board[(self.columns[start_col_index+1], start_row+1)][0] == 'b': legal_moves.append((self.columns[start_col_index+1], start_row+1))
            if start_col_index > 0:
                if self.chess_board[(self.columns[start_col_index-1], start_row+1)][0] == 'b': legal_moves.append((self.columns[start_col_index-1], start_row+1))
        
        else:
            #if one space forward is open add to set
            if self.chess_board[(start_col, start_row-1)] == 'o':
                legal_moves.append((start_col, start_row-1))
                #given one space open, if two spaces is open and starts at 2, add to set
                if self.chess_board[(start_col, start_row-2)] == 'o' and start_row == 7: legal_moves.append((start_col, start_row-2)) 
            
            #diagonals are white pieces that can be taken
            if start_col_index < 7:
                if self.chess_board[(self.columns[start_col_index-1], start_row-1)][0] == 'w': legal_moves.append((self.columns[start_col_index-1], start_row-1))
            if start_col_index > 0:
                if self.chess_board[(self.columns[start_col_index+1], start_row-1)][0] == 'w': legal_moves.append((self.columns[start_col_index+1], start_row-1))

        print("Pawn: ", legal_moves)
        return legal_moves
        
    def rookMoves(self, start, color):
        legal_moves = []
        left_distance = self.columns.index(start[0])+1
        right_distance = 9-left_distance
        down_distance = start[1]
        up_distance = 9-start[1]

        #add moves to the left
        for i in range(1, left_distance):
            col = self.colShift(start[0], -i)
            pos = (col, start[1])
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break
        
        #add moves to right
        for i in range(1, right_distance):
            col = self.colShift(start[0], i)
            pos = (col, start[1])
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break

        #add moves above
        for i in range(1, up_distance):
            row = start[1]+i
            pos = (start[0], row)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break
        
        #add moves below
        for i in range(1, down_distance):
            row = start[1]-i
            pos = (start[0], row)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break
        
        print("Rook: ", legal_moves)
        return legal_moves

    def bishopMoves(self, start, color):
        legal_moves = []
        left_distance = self.columns.index(start[0])+1
        right_distance = 9-left_distance
        down_distance = start[1]
        up_distance = 9-start[1]

        for i in range(1, min(left_distance, down_distance)): #left-down diagonal
            pos = (self.colShift(start[0], -i), start[1]-i)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break
        
        for i in range(1, min(right_distance, down_distance)): #right-down diagonal
            pos = (self.colShift(start[0], i), start[1]-i)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break

        for i in range(1, min(right_distance, up_distance)): #right-up diagonal
            pos = (self.colShift(start[0], i), start[1]+i)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break
        
        for i in range(1, min(left_distance, up_distance)): #left-up diagonal
            pos = (self.colShift(start[0], -i), start[1]+i)
            if self.chess_board[pos] == 'o':
                legal_moves.append(pos)
            elif self.chess_board[pos][0] != color:
                legal_moves.append(pos)
                break
            else:
                break

        print("Bishop: ", legal_moves)
        return legal_moves
    
    def knightMoves(self, start, color):
        legal_moves = []
        position_pairs = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1)] #list of possible knight move distances
        for (x, y) in position_pairs:
            pos = (self.colShift(start[0], x), start[1]+y)
            if pos[0] in self.columns and 0 < pos[1] < 9:
                if self.chess_board[pos][0] != color: legal_moves.append(pos)
        
        print("Knight: ", legal_moves)
        return legal_moves

    def queenMoves(self, start, color):
        return self.bishopMoves(start, color) + self.rookMoves(start, color)
    
    def kingMoves(self, start, color):
        legal_moves = []
        position_pairs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for (x, y) in position_pairs:
            pos = (self.colShift(start[0], x), start[1]+y)
            if pos[0] in self.columns and 0 < pos[1] < 9:
                if self.chess_board[pos][0] != color: legal_moves.append(pos)
        print("King: ", legal_moves)
        return True
    
    def getAllMoves(self, color):
        moves = []
        pieces = []
        for col in self.columns:
            for row in range(1,9):
                if self.chess_board[(col, row)][0] == color:
                    moves.append(self.legalMoves((col, row), color))
                    pieces.append((col, row))
        
        print("Pieces: ", pieces)
        print("Moves: ", moves)
        return pieces, moves
    
    def getValidMoves(self, moves, pieces):
        valid_moves = []
        for i in range(len(pieces)):
            for move in moves[i]:
                board_copy = self.chess_board
                self.move(pieces[i], move, board_copy)
                if not self.inCheck(self.turn, board_copy):
                    valid_moves.append(move)
        return valid_moves

    def startGame(self):        
        self.printBoard()
        while(not self.isCheckmate()):
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
            
            self.move(start, end, self.chess_board)
            self.printBoard()
            if self.turn == 'w':
                self.turn = 'b'
            else:
                self.turn = 'w'

        if(self.turn == 'w'):
            print("White Wins")
        else:
            print("Black Wins") 

    def inCheck(self, color, board):
        for col in self.columns: #check if king is currently in check
            for row in range(1,9):
                if board[(col, row)][0] != color and board[(col, row)][0] != 'o':
                    if color == 'w' and (self.white_king_pos in self.legalMoves((col, row), color)): #if king pos in possible moves for opposing color piece, you are in check
                        return True
                    elif color == 'b' and (self.black_king_pos in self.legalMoves((col, row), color)):
                        return True
        return False

    def isCheckmate(self):
        if self.kingMoves(self.white_king_pos, self.turn) == []:
            if self.inCheck:
                return True
        return False

        
        
