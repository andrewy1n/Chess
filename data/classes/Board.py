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

    def isInCheck(self, color: str, dummy_board) -> bool:

        king_pos = None
        
        for pos in dummy_board.squares: #find king position
            if dummy_board.squares[pos].occupying_piece is not None:
                piece = dummy_board.squares[pos].occupying_piece
                if piece.color == color and piece.notation == 'K':
                    king_pos = pos
        
        pieces = [s.occupying_piece for s in dummy_board.squares.values() if s.occupying_piece is not None]
        for piece in pieces:
            if piece.color == color:
                continue
            
            for square in piece.getPossibleMoves(dummy_board):
                if(square.c == king_pos[0] and square.r == king_pos[1]): #opposing piece can attack king
                    return True
        
        return False

    def isCheckMate(self, color) -> bool:
        possibleMoves = []
        for square in self.squares.values():
            piece = square.occupying_piece
            if(piece is not None and piece.color == color):
                possibleMoves.extend(piece.getValidMoves(self))
            
        return len(possibleMoves) == 0 and self.isInCheck(color, self)

    
    def isStaleMate(self) -> bool:
        whiteMoves = []
        blackMoves = []
        for square in self.squares.values():
            piece = square.occupying_piece
            if piece != None:
                if piece.color == 'w':
                    whiteMoves.extend(piece.getValidMoves(self))
                else:
                    blackMoves.extend(piece.getValidMoves(self))

        return len(whiteMoves) == len(blackMoves) == 0

    def printBoard(self) -> None:
        for row in self.rows[::-1]:
            for col in self.columns:
                piece = self.squares[(col, row)].occupying_piece
                print(piece.color + piece.notation, end=' ') if piece else print('-', end = '  ')
            print()