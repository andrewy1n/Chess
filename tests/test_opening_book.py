from data.classes.OpeningBook import OpeningBook
from data.classes.Board.Board import Board

book = OpeningBook("data/resources/Book.txt")
board = Board()

print(board.getCurrentFEN())
print(book.moves_by_position[board.getCurrentFEN()])

print(book.getMove(board))