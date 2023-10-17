import Piece
class Pawn(Piece):
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