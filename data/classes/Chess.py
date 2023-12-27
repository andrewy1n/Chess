from data.classes.Board import Board
import pygame
import sys

class Chess:
    def __init__(self, WIDTH=800, HEIGHT=800):
        pygame.init()
        self.board = Board("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
    
    def startGame(self):
        self.startScreen()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()
        
            self.drawBoard()

            if self.board.isCheckMate():
                if self.board.turn != 'w':
                    print('White Wins')
                else:
                    print('Black Wins')
                running = False
            elif self.board.isStaleMate():
                print('Stalemate')
                running = False
            
            pygame.display.flip()
    
    def startScreen(self):
        def drawText(text, font, color, surface, x, y):
            text_obj = font.render(text, True, color)
            text_rect = text_obj.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_obj, text_rect)
        
        def drawButton(text, font, color, button_color, surface, x, y, width, height):
            pygame.draw.rect(surface, button_color, (x, y, width, height))
            drawText(text, font, color, surface, x + width // 2, y + height // 2)
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (2, 50, 37)
        FONT_TITLE = pygame.font.Font(None, 54)
        FONT_SUBTITLE = pygame.font.Font(None, 24)
        FONT_BUTTON = pygame.font.Font(None, 36)
        BUTTON_WIDTH, BUTTON_HEIGHT = self.WIDTH // 4, self.HEIGHT // 12
        
        while True:
            self.screen.fill(GREEN)
            drawText("Chess Game", FONT_TITLE, WHITE, self.screen, self.WIDTH // 2, self.HEIGHT // 4)
            drawText("by Andrew Yin", FONT_SUBTITLE, WHITE, self.screen, self.WIDTH // 2, self.HEIGHT // 3)
            drawButton("2 Players", FONT_BUTTON, WHITE, BLACK, self.screen, self.WIDTH // 2 - BUTTON_WIDTH // 2, self.HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse_x <= self.WIDTH // 2 + BUTTON_WIDTH // 2 \
                            and self.HEIGHT // 2 <= mouse_y <= self.HEIGHT // 2 + BUTTON_HEIGHT:
                        return

            pygame.display.update()
  
    def handle_click(self) -> None:
        x, y = pygame.mouse.get_pos()
        r = 8 - y//100
        c = chr(x//100 + ord('a'))  
        square_selected =  self.board.squares[(c, r)]
        piece_selected = square_selected.occupying_piece
        
        if(self.board.highlighted_square is not None):
            highlighted_piece = self.board.highlighted_square.occupying_piece
            highlighted_square_pos = (self.board.highlighted_square.file, self.board.highlighted_square.rank)
            valid_moves = highlighted_piece.getValidMoves(self.board)
            for move in valid_moves:
                if move.target_square is square_selected:
                    self.board.makeMove(move)
                
            self.board.squares[highlighted_square_pos].is_highlighted = False
            self.board.highlighted_square = None
        
        elif piece_selected is not None and piece_selected.color == self.board.turn:
            square_selected.is_highlighted = True
            self.board.highlighted_square = square_selected
    
    def drawBoard(self) -> None:
        font = pygame.font.Font(None, 24)

        for square in self.board.squares.values():
            if square.is_highlighted:
                pygame.draw.rect(self.screen, (255, 244, 79), square.tile)
            else:
                pygame.draw.rect(self.screen, square.color, square.tile)

            if square.rank == 1:
                letter_color = (2, 50, 37) if square.color == (255, 255, 255) else (255, 255, 255)
                char = square.file.upper()

                letter = font.render(char, True, letter_color)
                letter_rect = letter.get_rect() 
                letter_rect.center = square.tile.center
                letter_rect.x += square.tile.width / 2.7
                letter_rect.y += square.tile.width / 2.7
                
                self.screen.blit(letter, letter_rect)
            
            if square.file == 'a':
                letter_color = (2, 50, 37) if square.color == (255, 255, 255) else (255, 255, 255)
                char = str(square.rank)

                letter = font.render(char, True, letter_color)
                letter_rect = letter.get_rect() 
                letter_rect.center = square.tile.center
                letter_rect.x -= square.tile.width / 2.7
                letter_rect.y -= square.tile.width / 2.7
                
                self.screen.blit(letter, letter_rect)
            
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                piece_image = None
                if piece.color == 'w':
                    piece_image = pygame.image.load(piece.white_piece_image_path)
                else:
                    piece_image = pygame.image.load(piece.black_piece_image_path)
                piece_image = pygame.transform.scale2x(piece_image)
                tile_center = (square.tile.centerx - square.tile.width//2 + 5, square.tile.centery - square.tile.height//2)
                self.screen.blit(piece_image, tile_center)
            
        if self.board.highlighted_square is not None:
            for move in self.board.highlighted_square.occupying_piece.getValidMoves(self.board):  
                pygame.draw.circle(self.screen, (150, 150, 150), move.target_square.tile.center, 20)