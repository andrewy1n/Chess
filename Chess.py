class Chess:
    def __init__(self):
        self.board = [['wr', 'wk', 'wb', 'wq', 'wk', 'wb', 'wk', 'wr'], 
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['br', 'bk', 'bb', 'bq', 'bk', 'bb', 'bk', 'br']]
        self.moveCount = 0
    def move(self, start, location):
        self.board[location[0]][location[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = 'o'
    def printBoard(self):
        print(self.board)

        
        
