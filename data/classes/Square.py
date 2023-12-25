from pygame import Rect
class Square:
    def __init__(self, file, rank) -> None:
        self.rank = rank
        self.file = file
        self.occupying_piece = None
        self.is_highlighted = False
        
        self.left = (ord(file)-ord('a')) * 100
        self.top = (8-rank) * 100
        self.color = (255, 255, 255) if (rank + ord(file)-ord('a')) % 2 == 0 else (1, 50, 32)
        self.tile = Rect((self.left, self.top), (100, 100))
        