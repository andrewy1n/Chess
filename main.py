from data.classes.Board import Board
import pygame

board = Board()
running = True
pygame.init()
screen = pygame.display.set_mode((800, 800))

pygame.display.set_caption('Chess')

if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click()
    
        board.drawBoard(screen)

        if board.isCheckMate():
            if board.turn == 'w':
                print('White Wins')
            else:
                print('Black Wins')
            running = False
        elif board.isStaleMate():
            print('Stalemate')
            running = False
        
        pygame.display.flip()