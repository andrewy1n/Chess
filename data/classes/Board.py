from data.classes.Square import Square
from data.classes.Pieces.Rook import Rook
from data.classes.Pieces.Bishop import Bishop
from data.classes.Pieces.Knight import Knight
from data.classes.Pieces.Queen import Queen
from data.classes.Pieces.King import King
from data.classes.Pieces.Pawn import Pawn
from collections import defaultdict


class Board:
    def __init__(self) -> None:
        self.squares = defaultdict(Square)
        self.columns = "abcdefgh"
        self.rows = list(range(1, 9))
        self.moves = [] #[color, fromSquare, toSquare, currBoard(COPY)]

        self.chess_board_config = self.generateBoard()

        self.initializeSquares()

    def generateBoard(self) -> dict:
        chess_board_dict = {
            ("a", 1): "wr",
            ("b", 1): "wn",
            ("c", 1): "wb",
            ("d", 1): "wq",
            ("e", 1): "wk",
            ("f", 1): "wb",
            ("g", 1): "wn",
            ("h", 1): "wr",
            ("a", 8): "br",
            ("b", 8): "bn",
            ("c", 8): "bb",
            ("d", 8): "bq",
            ("e", 8): "bk",
            ("f", 8): "bb",
            ("g", 8): "bn",
            ("h", 8): "br",
        }
        for c in self.columns:
            chess_board_dict[(c, 2)] = "wp"  # white pawns
            chess_board_dict[(c, 7)] = "bp"  # black pawns
        for r in range(3, 7):
            for c in self.columns:
                chess_board_dict[(c, r)] = "o"  # empty spaces
        return chess_board_dict

    def initializeSquares(self) -> None:
        for c in self.columns:
            for r in self.rows:
                self.squares[(c, r)] = Square(c, r)
                square = self.squares[(c, r)]
                if self.chess_board_config[(c, r)][0] != "o":
                    color = self.chess_board_config[(c, r)][0]
                    type = self.chess_board_config[(c, r)][1]

                    if type == "p":
                        square.occupying_piece = Pawn(color, (c, r))
                    elif type == "b":
                        square.occupying_piece = Bishop(color, (c, r))
                    elif type == "n":
                        square.occupying_piece = Knight(color, (c, r))
                    elif type == "r":
                        square.occupying_piece = Rook(color, (c, r))
                    elif type == "q":
                        square.occupying_piece = Queen(color, (c, r))
                    elif type == "k":
                        square.occupying_piece = King(color, (c, r))

    def isInCheck(self, color, board_change=None) -> bool:
        #Board changes are for validating chess board move, otherwise board state checker
        output = False

        king_pos = None
        prev_square_piece = None
        new_square_piece = None

        if board_change is not None: #board change, swap prev and new
            prev_square = self.squares[board_change[0]]
            new_square = self.squares[board_change[1]]
            prev_square_piece = prev_square.occupying_piece
            new_square_piece = new_square.occupying_piece
            new_square.occupying_piece = prev_square_piece
            prev_square.occupying_piece = new_square_piece
        
        pieces = [
            s.occupying_piece for s in self.squares.values() if s.occupying_piece
        ]

        for piece in pieces: #find king position
            if piece.color == color and piece.notation == "K":
                king_pos = piece.pos
        
        for piece in pieces:
            for move in piece.getPossibleMoves():
                if self.color != color and move.pos == king_pos: #opposing piece can attack king
                    output = True
        
        if board_change is not None: #swap positions back if board change
            prev_square.occupying_piece = prev_square_piece
            new_square.occupying_piece = new_square_piece
        
        return output

    def isCheckMate(self, color) -> bool:
        for square in self.squares.values():
            piece = square.occupying_piece
            if (piece != None and 
                piece.notation == 'K' and 
                piece.color == color):
                king = piece
    
        return king.getValidMoves() == [] and self.isInCheck()

    
    def isStaleMate(self) -> bool:
        for square in self.squares.values():
            piece = square.occupying_piece
            if piece != None and piece.notation == 'K':
                if piece.color == 'w':
                    white_king = piece
                else:
                    black_king = piece

        return (white_king.getValidMoves() == [] and 
                black_king.getValidMoves() == [] and 
                not self.isInCheck())

    def printBoard(self) -> None:
        for row in self.rows:
            for col in self.columns:
                piece = self.squares[(col, row)].occupying_piece
                print(piece.color + piece.notation, end=' ') if piece else print('-', end = '  ')
            print()