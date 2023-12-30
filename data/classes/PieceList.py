class PieceList:
    def __init__(self) -> None:
        self.white_pieces = set()
        self.black_pieces = set()
    
    def addPiece(self, piece):
        if piece.color == 'w':
            self.white_pieces.add(piece)
        else:
            self.black_pieces.add(piece)
    
    def removePiece(self, piece):
        if piece.color == 'w':
            self.white_pieces.remove(piece)
        else:
            self.black_pieces.remove(piece)
    
    def getAttackingSquares(self, color, board):
        output = []
        opposing_pieces = self.black_pieces if color == 'b' else self.white_pieces
        for attacking_piece in opposing_pieces:
            for move in attacking_piece.getAttackingMoves(board):
                output.append(move.target_pos)
        return output
    
    def getAllValidMoves(self, color, board):
        output = []
        for piece in self.black_pieces if color == 'b' else self.white_pieces:
            for move in piece.getValidMoves(board):
                output.append(move)
        return output

    def getAllPieces(self) -> set:
        return self.white_pieces.union(self.black_pieces)