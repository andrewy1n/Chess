from data.classes.Board.Square import Square
from data.classes.Board.Piece import Piece
from data.classes.Board.Move import Move
from data.classes.Board.PieceList import PieceList
from data.classes.Board.GameState import GameState
from data.classes.Board.Pieces.Rook import Rook
from data.classes.Board.Pieces.Bishop import Bishop
from data.classes.Board.Pieces.Knight import Knight
from data.classes.Board.Pieces.Queen import Queen
from data.classes.Board.Pieces.King import King
from data.classes.Board.Pieces.Pawn import Pawn
from collections import defaultdict
from data.classes.Bitboard import Bitboard

class Board:
    def __init__(self, FEN_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        self.squares = defaultdict(Square)
        self.files = "abcdefgh"
        self.ranks = list(range(1, 9))
        self.ordinals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.cardinals = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.move_history = []
        self.game_state_history = []
        self.current_game_state = None
        self.turn = 'w'
        self.highlighted_square = None

        self.piece_list = PieceList()

        self.white_king_pos = ('e', 1)
        self.black_king_pos = ('e', 8)

        self.full_moves = None

        self.initializeSquares()
        
        self.loadPositionfromFEN(FEN_string)
        

    def loadPositionfromFEN(self, fen: str):
        pieceTypeFromSymbol = {"p": Pawn, "b": Bishop, "n": Knight, "r": Rook, "q": Queen, "k": King}
        fen_parts = fen.split()
        
        positions, turn, castling_rights, enpassant_pos, *extra_parts = fen_parts
        half_moves = extra_parts[0] if extra_parts else '0'  # Default to '0' if not provided
        full_moves = extra_parts[1] if len(extra_parts) > 1 else '1'  # Default to '1' if not provided
        
        self.current_game_state = GameState(enpassant_pos, castling_rights, int(half_moves))
        self.game_state_history.append(self.current_game_state)
        self.turn = turn
        self.full_moves = int(full_moves)

        file, rank = 'a', 8
        for c in positions:
            if c == '/':
                file = 'a'
                rank -= 1
            else:
                if c.isnumeric():
                    file = chr(ord(file) + int(c))
                else:
                    pieceColor = 'w' if c.isupper() else 'b'
                    pieceType = pieceTypeFromSymbol.get(c.lower())
                    square = self.squares[(file, rank)] 
                    piece = pieceType(pieceColor, (file, rank))
                    square.occupying_piece = piece

                    self.piece_list.addPiece(piece)
                    file = chr(ord(file) + 1)
    
    def getCurrentFEN(self):
        fen = ""
        empty_count = 0
        for rank in self.ranks[::-1]:
            for file in self.files:
                square = self.squares[(file, rank)]
                if square.occupying_piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    piece = square.occupying_piece
                    fen += piece.notation.lower() if piece.color == 'b' else piece.notation
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            if rank > 1:
                fen += "/"
        
        return fen + " " + self.turn + " " + self.current_game_state.castling_rights + " -"
    
    def initializeSquares(self) -> None:
        for file in self.files:
            for rank in self.ranks:
                pos = (file, rank)
                self.squares[pos] = Square(file, rank)
    
    def makeMove(self, move: Move) -> None:
        """
        Makes a move on the board. If the move is permanent, piece's that are moved
        change their own positions. Non-permanent moves are meant to check for 
        move validity.
        """
        new_enpassant_pos = None
        new_castling_rights = self.current_game_state.castling_rights
        new_half_move_counter = self.current_game_state.half_move_counter

        #King Side Castling
        if move.is_king_side_castle:        
            self.piece_list.removePiece(move.king_side_rook)
            self.squares[('h', move.target_pos[1])].occupying_piece = None
            self.squares[('f', move.target_pos[1])].occupying_piece = move.king_side_rook
            
            move.king_side_rook.pos = ('f', move.target_pos[1])
            self.piece_list.addPiece(move.king_side_rook)

        #Queen Side Castling    
        elif move.is_queen_side_castle:
            self.piece_list.removePiece(move.queen_side_rook)
            self.squares[('a', move.target_pos[1])].occupying_piece = None
            self.squares[('d', move.target_pos[1])].occupying_piece = move.queen_side_rook
            
            move.queen_side_rook.pos = ('d', move.target_pos[1])
            self.piece_list.addPiece(move.queen_side_rook)
        
        #En Passant
        if move.is_enpassant:
            self.piece_list.removePiece(move.enpassant_pawn)
            move.enpassant_square.occupying_piece = None

        #Start Square has no piece    
        move.start_square.occupying_piece = None 
        
        #Remove that piece from the list
        self.piece_list.removePiece(move.start_piece)

        #Change the piece's position to target position
        moved_piece = move.start_piece
        moved_piece.pos = move.target_pos

        #Promotion
        if move.is_promotion:
            move.target_square.occupying_piece = move.promoted_piece
            self.piece_list.addPiece(move.promoted_piece)
        else:
            #Otherwise, normally occupy target square with moved piece and add to piece list
            move.target_square.occupying_piece = moved_piece
            self.piece_list.addPiece(moved_piece)

        if move.start_piece.notation == 'K':
            if move.start_piece.color == 'w':
                self.white_king_pos = move.target_pos
            else:
                self.black_king_pos = move.target_pos
        
        #If a piece is taken, remove them from their pieces set
        if move.target_piece is not None:
            self.piece_list.removePiece(move.target_piece)
        
        if self.turn == 'b':
            self.full_moves += 1

        self.turn = 'b' if self.turn == 'w' else 'w'
        
        if moved_piece.notation == 'K':
            if moved_piece.color == 'w':
                new_castling_rights = new_castling_rights.replace('K', "")
                new_castling_rights = new_castling_rights.replace('Q', "")
            else:
                new_castling_rights = new_castling_rights.replace('k', "")
                new_castling_rights = new_castling_rights.replace('q', "")
        
        if moved_piece.notation == 'R':
            if move.start_pos == ('a', 1):
                new_castling_rights = new_castling_rights.replace('Q', "")
            elif move.start_pos == ('h', 1):
                new_castling_rights = new_castling_rights.replace('K', "")
            elif move.start_pos == ('a', 8):
                new_castling_rights = new_castling_rights.replace('q', "")
            elif move.start_pos == ('h', 8):
                new_castling_rights = new_castling_rights.replace('k', "")
        
        if moved_piece.notation == 'P':
            new_half_move_counter = 0
        else:
            new_half_move_counter += 1
        
            
        self.move_history.append(move)

        new_state = GameState(new_enpassant_pos, new_castling_rights, new_half_move_counter)
        self.game_state_history.append(new_state)
        self.current_game_state = new_state

    def unmakeMove(self, move: Move):
        """
        Undo a move, essentially the inverse of makeMove.
        """
        #King Side Castling
        if move.is_king_side_castle:        
            self.piece_list.removePiece(move.king_side_rook)
            self.squares[('h', move.start_pos[1])].occupying_piece = move.king_side_rook
            self.squares[('f', move.start_pos[1])].occupying_piece = None
            move.king_side_rook.pos = ('h', move.start_pos[1])
            self.piece_list.addPiece(move.king_side_rook)

        #Queen Side Castling    
        elif move.is_queen_side_castle:
            self.piece_list.removePiece(move.queen_side_rook)
            self.squares[('a', move.start_pos[1])].occupying_piece = move.queen_side_rook
            self.squares[('d', move.start_pos[1])].occupying_piece = None
            move.queen_side_rook.pos = ('a', move.start_pos[1])
            self.piece_list.addPiece(move.queen_side_rook)
        
        #En Passant
        if move.is_enpassant:
            move.enpassant_square.occupying_piece = move.enpassant_pawn
            self.piece_list.addPiece(move.enpassant_pawn)
        
        #If pawn promoted, remove promoted piece, else remove moved_piece
        if move.is_promotion:
            self.piece_list.removePiece(move.promoted_piece)
        else:
            moved_piece = move.start_piece
            self.piece_list.removePiece(moved_piece)
        
        #Return Start piece to start position
        move.start_piece.pos = move.start_pos
        
        #Return start and target squares and their own pieces
        move.start_square.occupying_piece = move.start_piece
        move.target_square.occupying_piece = move.target_piece
        
        #Add back start piece back to piece list
        self.piece_list.addPiece(move.start_piece)

        #If a piece was captured, return piece back to piece list
        if move.target_piece is not None:
            self.piece_list.addPiece(move.target_piece)
        
        if move.start_piece.notation == 'K':
            if move.start_piece.color == 'w':
                self.white_king_pos = move.start_pos
            else:
                self.black_king_pos = move.start_pos
        
        self.turn = 'b' if self.turn == 'w' else 'w'

        if self.turn == 'b':
            self.full_moves -= 1

        self.game_state_history.pop()
        self.move_history.pop()

        self.current_game_state = self.game_state_history[-1]
        
    def isInCheck(self, color) -> bool:
        king_pos = self.white_king_pos if color == 'w' else self.black_king_pos
        
        return king_pos in self.piece_list.getAttackingSquares('b' if color == 'w' else 'w', self)
        
    def isCheckMate(self) -> bool:
        if not self.isInCheck(self.turn):
            return False
  
        return len(self.piece_list.getAllValidMoves(self.turn, self)) == 0

    def isStaleMate(self) -> bool:        
        white_moves = self.piece_list.getAllValidMoves('w', self)
        black_moves = self.piece_list.getAllValidMoves('b', self)
        return ((len(white_moves) == 0 or len(black_moves) == 0) and not self.isInCheck(self.turn)) or self.current_game_state.half_move_counter >= 100
    
    #Prints basic text board
    def printBoard(self) -> None:
        for rank in self.ranks[::-1]:
            for file in self.files:
                piece = self.squares[(file, rank)].occupying_piece
                print(piece.color + piece.notation, end=' ') if piece else print('-', end = '  ')
            print()