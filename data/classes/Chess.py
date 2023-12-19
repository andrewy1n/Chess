from data.classes.Board import Board
import pygame
import sys

class Chess:
    def __init__(self, WIDTH=800, HEIGHT=800):
        pygame.init()
        self.board = Board()
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
                    self.board.handle_click()
        
            self.board.drawBoard(self.screen)

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
  
        
        
