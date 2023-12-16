from pygame import Rect
class Square:
    def __init__(self, c, r) -> None:
        self.r = r
        self.c = c
        self.occupying_piece = None
        self.is_highlighted = False
        
        self.left = (ord(c)-ord('a')) * 100
        self.top = (8-r) * 100
        self.color = (255, 255, 255) if (r + ord(c)-ord('a')) % 2 == 0 else (1, 50, 32)
        self.tile = Rect((self.left, self.top), (100, 100))
        