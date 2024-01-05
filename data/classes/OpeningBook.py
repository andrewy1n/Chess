from data.classes.Board.Move import Move
from data.classes.Board.Board import Board
import random

class OpeningBook:
    def __init__(self, file: str) -> None:
        self.moves_by_position = {}

        with open(file, 'r') as file:
            file_content = file.read()

        self.entries = file_content.strip(' \n').split("pos")[1:]
        
        for entry in self.entries:
            entry_data = entry.strip('\n').split('\n')
            position_fen = entry_data[0].strip()
            all_move_data = entry_data[1:]

            book_moves = []

            for move_data in all_move_data:
                move_split = move_data.split(' ')
                move = move_split[0]
                occurences = move_split[1]
                
                book_moves.append((move, occurences))

            self.moves_by_position[position_fen] = book_moves
    
    def hasMove(self, board: Board) -> bool:
        return board.getCurrentFEN() in self.moves_by_position
    
    def getMove(self, board: Board) -> Move:
        fen_str = board.getCurrentFEN()
        book_moves = self.moves_by_position[fen_str]
        total = 0
        
        for move, occ in book_moves:
            total += int(occ)

        weights = []
        weight_sum = 0

        for move, occ in book_moves:
            weight = int(occ)/total
            weight_sum += weight
            weights.append(weight)
        
        prob_cumul = [sum(weights[max(0, i - 1): i + 1]) / weight_sum for i in range(len(weights))]

        for i, move in enumerate(book_moves):
            random_val = random.random()
            if random_val <= prob_cumul[i]:
                return move[0]
            

