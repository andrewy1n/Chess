from Pieces import Rook
from Pieces import Bishop
from Pieces import Knight
from Pieces import Queen
from Pieces import King
from Pieces import Pawn
import Square
from collections import defaultdict


class Board:
    def __init__(self) -> None:
        self.chess_board = self.generateBoard()
        self.squares = defaultdict(Square)
        self.columns = "abcdefgh"
        self.rows = list(range(1, 9))

        self.initializeBoard()

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

    def initializeBoard(self) -> None:
        for c in self.columns:
            for r in self.rows:
                self.squares[(c, r)] = Square(c, r)
                square = self.squares[(r, c)]
                if self.chess_board[c, r][0] != "o":
                    color = self.chess_board[(c, r)][0]
                    type = self.chess_board[(c, r)][1]

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
