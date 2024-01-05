class Evaluation:
    chess_value_dict = {
        'P' : 100,
        'N' : 300,
        'B' : 300,
        'R' : 500,
        'Q' : 900,
        'K' : 0
    }

    def evaluate(board):
        white_eval = Evaluation.countMaterial(board.piece_list.white_pieces)
        black_eval = Evaluation.countMaterial(board.piece_list.black_pieces)

        evaluation = white_eval - black_eval

        perspective = 1 if board.turn == 'w' else -1

        return evaluation * perspective 

    
    def countMaterial(pieces: list):
        score = 0
        for piece in pieces:
            if piece.notation == 'K':
                continue
            score += Evaluation.chess_value_dict[piece.notation]
        return score
