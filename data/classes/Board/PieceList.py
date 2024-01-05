from data.classes.Evaluation import Evaluation

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
    
    def getOrderedMoves(self, color, board):
        output = []

        for piece in self.black_pieces if color == 'b' else self.white_pieces:
            piece_value = Evaluation.chess_value_dict[piece.notation]
            for move in piece.getValidMoves(board):
                score = 0

                if move.target_piece is not None:
                    target_piece_value = Evaluation.chess_value_dict[move.target_piece.notation]
                    capture_score = target_piece_value - piece_value
                    if capture_score > 0:
                        score += 500 + capture_score
                    else:
                        score += capture_score
                
                if move.start_piece.notation == 'P' and move.is_promotion and move.promoted_piece.notation == 'Q':
                    score += 1000
                
                output.append((-score, move))
        
        return sorted(output, key=lambda x: x[0])

    def getAllPieces(self) -> set:
        return self.white_pieces.union(self.black_pieces)