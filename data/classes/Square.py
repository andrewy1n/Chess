class Square:
    def __init__(self, file, rank) -> None:
        self.rank = rank
        self.file = file
        self.occupying_piece = None
        