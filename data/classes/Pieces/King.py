from data.classes.Piece import Piece
from data.classes.Move import Move

class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"
        self.has_moved = False
        self.black_piece_image_path  = 'data/images/king-b.svg'
        self.white_piece_image_path  = 'data/images/king-w.svg'

    def getPossibleMoves(self, board) -> list:
        output = []
        
        output.extend(self.getAttackingMoves(board))
        
        if(not self.has_moved
            and not board.isInCheck(self.color)):
            rookRow = self.pos[1]
            opposing_moves = board.piece_list.getAttackingSquares('b' if self.color == 'w' else 'w', board)

            #king side castling
            if (board.squares[('h', rookRow)].occupying_piece is not None and 
                board.squares[('h', rookRow)].occupying_piece.notation == 'R' and 
                not board.squares[('h', rookRow)].occupying_piece.has_moved and 
                board.squares[('f', rookRow)].occupying_piece is None and 
                board.squares[('g', rookRow)].occupying_piece is None and 
                ('f', rookRow) not in opposing_moves):
                
                move = Move(board.squares[self.pos], board.squares[('g', rookRow)])
                move.is_king_side_castle = True
                move.king_side_rook = board.squares[('h', rookRow)].occupying_piece
                
                output.append(move)
            
            #queen side castling
            if (board.squares[('a', rookRow)].occupying_piece is not None and
                board.squares[('a', rookRow)].occupying_piece.notation == 'R' and 
                not board.squares[('a', rookRow)].occupying_piece.has_moved and 
                board.squares[('c', rookRow)].occupying_piece is None and 
                board.squares[('b', rookRow)].occupying_piece is None and 
                board.squares[('d', rookRow)].occupying_piece is None and
                ('d', rookRow) not in opposing_moves):
               
                move = Move(board.squares[self.pos], board.squares[('c', rookRow)])
                move.is_queen_side_castle = True
                move.queen_side_rook = board.squares[('a', rookRow)].occupying_piece
                
                output.append(move) 
        
        return output
    
    def getAttackingMoves(self, board):
        return super().generateDirectionalMoves(board, board.cardinals + board.ordinals, repeated=False)