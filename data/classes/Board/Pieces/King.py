from data.classes.Board.Piece import Piece
from data.classes.Board.Move import Move

class King(Piece):
    def __init__(self, color, pos) -> None:
        super().__init__(color, pos)
        self.notation = "K"
        self.black_piece_image_path  = 'data/images/king-b.png'
        self.white_piece_image_path  = 'data/images/king-w.png'

    def getPossibleMoves(self, board) -> list:
        output = []
        
        output.extend(self.getAttackingMoves(board))
        
        if(not board.isInCheck(self.color)):
            rookRow = self.pos[1]
            opposing_moves = board.piece_list.getAttackingSquares('b' if self.color == 'w' else 'w', board)
            
            #king side castling
            if (((self.color == 'w' and 'K' in board.current_game_state.castling_rights) or
                 (self.color == 'b' and 'k' in board.current_game_state.castling_rights)) and
                board.squares[('h', rookRow)].occupying_piece is not None and 
                board.squares[('h', rookRow)].occupying_piece.notation == 'R' and 
                board.squares[('f', rookRow)].occupying_piece is None and 
                board.squares[('g', rookRow)].occupying_piece is None and 
                ('f', rookRow) not in opposing_moves):
                
                move = Move(board.squares[self.pos], board.squares[('g', rookRow)])
                move.is_king_side_castle = True
                move.king_side_rook = board.squares[('h', rookRow)].occupying_piece
                
                output.append(move)
            
            #queen side castling
            if (((self.color == 'w' and 'Q' in board.current_game_state.castling_rights) or
                 (self.color == 'b' and 'q' in board.current_game_state.castling_rights)) and
                 board.squares[('a', rookRow)].occupying_piece is not None and
                board.squares[('a', rookRow)].occupying_piece.notation == 'R' and
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