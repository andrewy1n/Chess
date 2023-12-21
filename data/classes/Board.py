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
        self.files = "abcdefgh"
        self.ranks = list(range(1, 9))
        self.moves = [] #[color, fromSquare, toSquare, curr_squares]
        self.turn = 'w'
        self.highlighted_square = None

        start_FEN_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.initializeSquares()
        self.loadPositionfromFEN(start_FEN_string)

        self.white_attacking_squares = self.loadAttackingSquares('w')
        self.black_attacking_squares = self.loadAttackingSquares('b')

    def loadPositionfromFEN(self, fen: str):
        pieceTypeFromSymbol = {"p": Pawn, "b": Bishop, "n": Knight, "r": Rook, "q": Queen, "k": King}
        
        file, rank = 'a', 8
        for c in list(fen):
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
                    square.occupying_piece = pieceType(pieceColor, (file, rank))
                    file = chr(ord(file) + 1)
    
    def loadAttackingSquares(self, color):
        output = []
        for square in self.squares.values():
            piece = square.occupying_piece
            if piece is not None and piece.color == color:
                output.extend(piece.getPossibleMoves(self.squares, self.moves))
        return output
    
    def initializeSquares(self) -> None:
        for file in self.files:
            for rank in self.ranks:
                self.squares[(file, rank)] = Square(file, rank)

    def isInCheck(self, color: str, squares: dict) -> bool:
        king_pos = None
        
        for pos in squares: #find king position
            if squares[pos].occupying_piece is not None:
                piece = squares[pos].occupying_piece
                if piece.color == color and piece.notation == 'K':
                    king_pos = pos
        
        return self.isAttacked(color, king_pos, squares)
    
    def isAttacked(self, color: str, pos: tuple, squares: dict) -> bool:
        for square in squares.values():
            piece = square.occupying_piece
            if piece is not None and piece.color != color:
                for attacked_square in piece.getPossibleMoves(squares, self.moves):
                    if(attacked_square.c == pos[0] and attacked_square.r == pos[1]):
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

        return len(whiteMoves) == 0 or len(blackMoves) == 0

    def printBoard(self) -> None:
        for rank in self.ranks[::-1]:
            for file in self.files:
                piece = self.squares[(file, rank)].occupying_piece
                print(piece.color + piece.notation, end=' ') if piece else print('-', end = '  ')
            print()
    
    def drawBoard(self, screen) -> None:
        font = pygame.font.Font(None, 24)

        for square in self.squares.values():
            if square.is_highlighted:
                pygame.draw.rect(screen, (255, 244, 79), square.tile)
            else:
                pygame.draw.rect(screen, square.color, square.tile)

            if square.r == 1:
                letter_color = (2, 50, 37) if square.color == (255, 255, 255) else (255, 255, 255)
                char = square.c.upper()

                letter = font.render(char, True, letter_color)
                letter_rect = letter.get_rect() 
                letter_rect.center = square.tile.center
                letter_rect.x += square.tile.width / 2.7
                letter_rect.y += square.tile.width / 2.7
                
                screen.blit(letter, letter_rect)
            
            if square.c == 'a':
                letter_color = (2, 50, 37) if square.color == (255, 255, 255) else (255, 255, 255)
                char = str(square.r)

                letter = font.render(char, True, letter_color)
                letter_rect = letter.get_rect() 
                letter_rect.center = square.tile.center
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
                pygame.draw.circle(screen, (150, 150, 150), square.tile.center, 20)
        
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
                self.squares = highlighted_piece.move((c, r), self, permanent = True)
                self.moves.append([deepcopy(self.turn), deepcopy(self.squares[highlighted_square_pos]), deepcopy(self.squares[(c, r)]), deepcopy(self.squares)])
                self.turn = 'b' if self.turn == 'w' else 'w'
                
            self.squares[highlighted_square_pos].is_highlighted = False
            self.highlighted_square = None
        
        elif piece_selected is not None and piece_selected.color == self.turn:
            square_selected.is_highlighted = True
            self.highlighted_square = square_selected