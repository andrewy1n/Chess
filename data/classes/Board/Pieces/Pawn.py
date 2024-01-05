from data.classes.Board.Piece import Piece
from data.classes.Board.Move import Move
from data.classes.Board.Pieces.Bishop import Bishop
from data.classes.Board.Pieces.Knight import Knight
from data.classes.Board.Pieces.Rook import Rook
from data.classes.Board.Pieces.Queen import Queen

class Pawn(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "P"
        self.promotion_list = [Bishop, Knight, Rook, Queen]
        self.black_piece_image_path  = 'data/images/pawn-b.png'
        self.white_piece_image_path  = 'data/images/pawn-w.png'

    def getPossibleMoves(self, board) -> list:
        output = []
        
        #white and black different conditions color positional modifier
        cm = 1 if self.color != 'b' else -1
        
        forward_one = (self.pos[0], self.pos[1] + cm)
        forward_two = (self.pos[0], self.pos[1] + 2*cm)

        #Pawn Forward Moves
        if(forward_one[1] in range(1,9) and 
           board.squares[forward_one].occupying_piece is None):
            if forward_one[1] == 1 or forward_one[1] == 8:
                output.extend(self.appendPromotingMoves(board.squares[forward_one], board))
            else:    
                output.append(Move(board.squares[self.pos], board.squares[forward_one]))
            
            if(((self.pos[1] == 2 and self.color == 'w') or 
               (self.pos[1] == 7 and self.color == 'b')) and
                board.squares[forward_two].occupying_piece is None):
                move = Move(board.squares[self.pos], board.squares[forward_two])
                move.enpassant_flag = True
                output.append(move) 
        
        #Diagonals are opposing pieces that can be taken
        for attacking_move in self.getAttackingMoves(board):     
            if attacking_move.target_piece is not None and attacking_move.target_piece.color != self.color:
                if attacking_move.target_pos[1] == 8 or attacking_move.target_pos[1] == 1:
                    output.extend(self.appendPromotingMoves(attacking_move.target_square, board))
                else:
                    output.append(attacking_move)
        
        #En Passant
        pawn_rank = 5 if self.color == 'w' else 4
        
        if(self.pos[1] == pawn_rank and len(board.move_history) > 0):
            prev_move =  board.move_history[-1]
            pawn_dist = ord(prev_move.target_square.file) - ord(self.pos[0])     
            diagonal_move = (super().columnShift(self.pos[0], pawn_dist), self.pos[1] + cm)

            if prev_move.enpassant_flag and abs(pawn_dist) == 1:
                move = Move(board.squares[self.pos], board.squares[diagonal_move])
                move.is_enpassant = True
                move.enpassant_pawn = prev_move.start_piece
                move.enpassant_square = prev_move.target_square
                output.append(move)

        return output
    
    def getAttackingMoves(self, board):
        cm = 1 if self.color == 'w' else -1
        directions = [(1, 1 * cm), (-1, 1 * cm)]

        return super().generateDirectionalMoves(board, directions, repeated=False)
    
    def appendPromotingMoves(self, target_square, board):
        output = []
        for piece in self.promotion_list:
            move = Move(board.squares[self.pos], target_square)
            move.is_promotion = True
            move.promoted_piece = piece(self.color, move.target_pos)
            output.append(move)
        return output