from data.classes.Square import Square
from data.classes.Pieces.Rook import Rook
from data.classes.Pieces.Bishop import Bishop
from data.classes.Pieces.Knight import Knight
from data.classes.Pieces.Queen import Queen
from data.classes.Pieces.King import King
from data.classes.Pieces.Pawn import Pawn
from collections import defaultdict
from copy import deepcopy
import pygame


class Board:
    def __init__(self) -> None:
        self.squares = defaultdict(Square)
        self.columns = "abcdefgh"
        self.rows = list(range(1, 9))
        self.moves = [] #[color, fromSquare, toSquare, curr_squares]
        self.turn = 'w'
        self.highlighted_square = None

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

    def isInCheck(self, color: str, dummy_squares: dict) -> bool:

        king_pos = None
        
        for pos in dummy_squares: #find king position
            if dummy_squares[pos].occupying_piece is not None:
                piece = dummy_squares[pos].occupying_piece
                if piece.color == color and piece.notation == 'K':
                    king_pos = pos
        
        pieces = [s.occupying_piece for s in dummy_squares.values() if s.occupying_piece is not None]
        for piece in pieces:
            if piece.color == color:
                continue
            
            for square in piece.getPossibleMoves(dummy_squares, self.moves):
                if(square.c == king_pos[0] and square.r == king_pos[1]): #opposing piece can attack king
                    return True
        
        return False

    def isCheckMate(self) -> bool:
        possibleMoves = []
        for square in self.squares.values():
            piece = square.occupying_piece
            if(piece is not None and piece.color == self.turn):
                possibleMoves.extend(piece.getValidMoves(self))
            
        return len(possibleMoves) == 0 and self.isInCheck(self.turn, self.squares)

    
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
    
    def drawBoard(self, screen) -> None:
        font = pygame.font.Font(None, 24)

        for square in self.squares.values():
            if square.is_highlighted:
                pygame.draw.rect(screen, (255, 244, 79), square.tile)
            else:
                pygame.draw.rect(screen, square.color, square.tile)

            if square.r == 1 or square.c == 'a':
                letter_color = (2, 50, 37) if square.color == (255, 255, 255) else (255, 255, 255)
                char = square.c.upper() if square.r == 1 else str(square.r)

                letter = font.render(char, True, letter_color)
                letter_rect = letter.get_rect() 
                letter_rect.center = square.tile.center
                if square.r == 1:
                    letter_rect.x += square.tile.width / 2.7
                    letter_rect.y += square.tile.width / 2.7
                else:
                    letter_rect.x -= square.tile.width / 2.7
                    letter_rect.y -= square.tile.width / 2.7
                
                screen.blit(letter, letter_rect)
            
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                piece_image = None
                if piece.color == 'w':
                    piece_image = pygame.image.load(piece.white_piece_image_path)
                else:
                    piece_image = pygame.image.load(piece.black_piece_image_path)
                piece_image = pygame.transform.scale2x(piece_image)
                tile_center = (square.tile.centerx - square.tile.width//2 + 5, square.tile.centery - square.tile.height//2)
                screen.blit(piece_image, tile_center)
            
        if self.highlighted_square is not None:
            for square in self.highlighted_square.occupying_piece.getValidMoves(self):  
                pygame.draw.circle(screen, (0,0,0), square.tile.center, 20)
        
    def handle_click(self) -> None:
        x, y = pygame.mouse.get_pos()
        r = 8 - y//100
        c = chr(x//100 + ord('a'))
        square_selected =  self.squares[(c, r)]
        piece_selected = square_selected.occupying_piece
        
        if(self.highlighted_square is not None):
            highlighted_piece = self.highlighted_square.occupying_piece
            highlighted_square_pos = (self.highlighted_square.c, self.highlighted_square.r)
            if square_selected in highlighted_piece.getValidMoves(self):
                self.squares = highlighted_piece.move((c, r), self.squares, permanent = True)
                self.moves.append([deepcopy(self.turn), deepcopy(self.squares[highlighted_square_pos]), deepcopy(self.squares[(c, r)]), deepcopy(self.squares)])
                self.turn = 'b' if self.turn == 'w' else 'w'
                
            self.squares[highlighted_square_pos].is_highlighted = False
            self.highlighted_square = None
        
        elif piece_selected is not None and piece_selected.color == self.turn:
            square_selected.is_highlighted = True
            self.highlighted_square = square_selected
            
                
        

