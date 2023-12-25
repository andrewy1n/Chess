from data.classes.Square import Square
from data.classes.Piece import Piece
from data.classes.Move import Move
from data.classes.PieceList import PieceList
from data.classes.Pieces.Rook import Rook
from data.classes.Pieces.Bishop import Bishop
from data.classes.Pieces.Knight import Knight
from data.classes.Pieces.Queen import Queen
from data.classes.Pieces.King import King
from data.classes.Pieces.Pawn import Pawn
from collections import defaultdict

class Board:
    def __init__(self, FEN_string=None) -> None:
        self.squares = defaultdict(Square)
        self.files = "abcdefgh"
        self.ranks = list(range(1, 9))
        self.ordinals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.cardinals = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.move_history = []
        self.turn = 'w'
        self.highlighted_square = None

        self.piece_list = PieceList()

        self.white_king_pos = ('e', 1)
        self.black_king_pos = ('e', 8)

        start_FEN_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.initializeSquares()
        if FEN_string is None:
            self.loadPositionfromFEN(start_FEN_string)
        else:
            self.loadPositionfromFEN(FEN_string)


    def loadPositionfromFEN(self, fen: str):
        pieceTypeFromSymbol = {"p": Pawn, "b": Bishop, "n": Knight, "r": Rook, "q": Queen, "k": King}

        file, rank = 'a', 8
        for c in fen:
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
        
        self.turn = 'b' if self.turn == 'w' else 'w'
        
        #TODO fix this
        if (move.start_piece.notation == 'K' or move.start_piece.notation == 'R'):
            move.start_piece.has_moved = True
            
        self.move_history.append(move)

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

        #TODO fix this
        if (move.start_piece.notation == 'K' or move.start_piece.notation == 'R'):
            move.start_piece.has_moved = False
            
        self.move_history.pop()
        
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
        return (len(white_moves) == 0 or len(black_moves) == 0) and not self.isInCheck(self.turn)
    
    #Prints basic text board
    def printBoard(self) -> None:
        for rank in self.ranks[::-1]:
            for file in self.files:
                piece = self.squares[(file, rank)].occupying_piece
                print(piece.color + piece.notation, end=' ') if piece else print('-', end = '  ')
            print()