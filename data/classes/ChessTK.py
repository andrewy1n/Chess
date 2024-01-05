from data.classes.Board.Board import Board
from data.classes.Bot import Bot
import tkinter as tk
from PIL import Image, ImageTk

class Chess:
    def __init__(self, WIDTH=800, HEIGHT=800, SQUARE_SIZE=100) -> None:
        self.window = tk.Tk()
        self.window.title("Chess")
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.board = Board()
        self.square_size = SQUARE_SIZE
        
        self.bot = Bot()
        
        # Colors
        self.light_square = "#FFCE9E"
        self.dark_square = "#D18B47"
        self.light_blue_highlight = '#52B2BF'
        self.dark_blue_highlight = '#0073CF'

        #Piece and Move Information
        self.piece_inital_position = None
        self.highlighted_piece = None
        self.piece_selected = None
        self.valid_moves = {}
        
        # Piece Image Dict
        self.piece_images = {}

        # Piece ID Dict
        self.pieceIDs = {}

    def startGame(self):
        self.drawBoard()
        self.drawPieces()

        tk.mainloop()

    def drawBoard(self):
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                # Alternate square colors
                fill_color = self.light_square if (row + col) % 2 == 0 else self.dark_square

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
                
    def drawPieces(self):
        # Load images of chess pieces
        for piece in self.board.piece_list.getAllPieces():
            self.createPiece(piece)
    
    def createSquare(self, file, rank, color, tag=None):
        x1 = (ord(file) - ord('a')) * self.square_size
        y1 = (8 - rank) * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=tag)

    def createPiece(self, piece):
        # Open image from piece image path
        img = Image.open(piece.white_piece_image_path) if piece.color == 'w' else Image.open(piece.black_piece_image_path)
        
        # Resize image to square size
        img_resized = img.resize((self.square_size, self.square_size), Image.LANCZOS)
        
        # Convert image to TK photo image
        img_tk = ImageTk.PhotoImage(img_resized)

        # Get Canvas Position
        x, y = self.squarePosToCanvasPos(piece.pos)

        self.piece_images[piece] = img_tk

        #Create Piece Image onto Canvas
        piece_image = self.canvas.create_image(x, y, anchor=tk.CENTER, image=img_tk, tag="pieces")
        
        #Bind Dragging to Piece Image
        self.canvas.tag_bind(piece_image, "<Button-1>", self.startDrag)
        self.canvas.tag_bind(piece_image, "<B1-Motion>", self.pieceDrag)
        self.canvas.tag_bind(piece_image, "<ButtonRelease-1>", self.stopDrag)

        #Add Piece Image to PieceID dict
        self.pieceIDs[piece] = piece_image

    def startDrag(self, event):
        piece_id = event.widget.find_withtag(tk.CURRENT)[0]
        self.piece_inital_position = event.widget.coords(piece_id)

        file, rank = self.canvasPosToSquarePos((event.x, event.y))

        square_selected = self.board.squares[(file, rank)]
        self.piece_selected = square_selected.occupying_piece
            
        if self.piece_selected is not None and self.piece_selected.color == self.board.turn:
            self.canvas.delete("highlight")
            self.getAndDrawValidMoves(self.piece_selected)
            self.highlighted_piece = self.piece_selected
        
        event.widget.drag_data = {"piece_id": piece_id, "x": event.x, "y": event.y}
    
    def pieceDrag(self, event):
        if self.highlighted_piece is None or \
            self.piece_selected is not None and self.piece_selected.color != self.board.turn:
            return

        self.canvas.coords(tk.CURRENT, event.x, event.y)

    def stopDrag(self, event):
        widget = event.widget
        piece_id = widget.drag_data["piece_id"]

        file, rank = self.canvasPosToSquarePos((event.x, event.y))

        # Handle Non-Valid Moves, return piece to initial position
        if self.highlighted_piece is None or \
            not self.highlighted_piece.isInBound(file, rank) or \
                len(self.valid_moves) == 0 or \
                    (file, rank) not in self.valid_moves or \
                        self.piece_selected is not None and self.piece_selected.color != self.board.turn:
            widget.coords(piece_id, self.piece_inital_position[0], self.piece_inital_position[1])
            return
        
        # If Move is a Promotion Handle User Input Promotion
        elif self.valid_moves[(file, rank)].is_promotion:
            promoted_piece_notation = self.promptPromotion()
            for move in self.valid_moves.values():
                if move.is_promotion and move.promoted_piece.notation == promoted_piece_notation:
                    self.movePiece(move)

                    x, y = self.squarePosToCanvasPos((file, rank))

                    widget.coords(piece_id, x, y)
                    break
        else:
            move = self.valid_moves[(file, rank)]
            self.movePiece(move)

            x, y = self.squarePosToCanvasPos((file, rank))

            widget.coords(piece_id, x, y)
        
        self.highlighted_piece = None
        self.valid_moves.clear()
        self.canvas.delete("highlight")

        if self.board.isCheckMate():
            winner = 'White' if self.board.turn == 'b' else 'Black'
            self.displayWinner(winner)
            return
        elif self.board.isStaleMate():
            self.displayWinner("Nobody")
            return
   
        self.botMove()
    
    def botMove(self):
        evaluation, move = self.bot.getBestMove(self.board)
        piece_pos = move.target_pos
        x, y = self.squarePosToCanvasPos(piece_pos)
        piece_image = self.pieceIDs[move.start_piece]
        self.canvas.coords(piece_image, x, y)
        self.movePiece(move)
        
        if self.board.isCheckMate():
            winner = 'White' if self.board.turn == 'b' else 'Black'
            self.displayWinner(winner)
        elif self.board.isStaleMate():
            self.displayWinner("Nobody")
    
    def movePiece(self, move):
        self.board.makeMove(move)
        if move.is_king_side_castle:
            rook_position = move.king_side_rook.pos
            x, y = self.squarePosToCanvasPos(rook_position)
            rook_image = self.pieceIDs[move.king_side_rook]
            self.canvas.coords(rook_image, x, y)
        
        if move.is_queen_side_castle:
            rook_position = move.queen_side_rook.pos
            x, y = self.squarePosToCanvasPos(rook_position)
            rook_image = self.pieceIDs[move.queen_side_rook]
            self.canvas.coords(rook_image, x, y)
        
        if move.target_piece is not None:
            taken_piece = self.pieceIDs[move.target_piece]
            self.canvas.delete(taken_piece)
        
        if move.is_enpassant:
            enpassant_pawn = self.pieceIDs[move.enpassant_pawn]
            self.canvas.delete(enpassant_pawn)
        
        if move.is_promotion:
            promoted_piece = move.promoted_piece
            initial_pawn = self.pieceIDs[move.start_piece]
            self.canvas.delete(initial_pawn)
            self.createPiece(promoted_piece)
    
    def promptPromotion(self):
        promotion_window = tk.Toplevel(self.window)
        promotion_window.title("Choose Promotion")
        
        # Assuming available promoted pieces are Queen, Rook, Bishop, Knight
        promoted_pieces = ['Q', 'R', 'B', 'N']  # Notation updated for Knight
        
        chosen_piece = None  # Variable to store the chosen piece
        
        def handlePromotionChoice(piece):
            nonlocal chosen_piece
            chosen_piece = piece
            promotion_window.destroy()  # Close the promotion window

        for piece in promoted_pieces:
            piece_button = tk.Button(promotion_window, text=piece, command=lambda p=piece: handlePromotionChoice(p))
            piece_button.pack()

        promotion_window.wait_window()  # Wait for the user to make a choice before proceeding
        return chosen_piece
    
    def displayWinner(self, winner):
        # Calculate the center of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = (screen_width - 400) // 2  # Assuming the pop-up width is 400
        center_y = (screen_height - 200) // 2  # Assuming the pop-up height is 200

        # Create a new window to display the winner at the calculated center position
        winner_window = tk.Toplevel(self.window)
        winner_window.title("Game Over")
        winner_window.geometry(f"400x200+{center_x}+{center_y}")

        # Display the winner on a label
        winner_label = tk.Label(winner_window, text=f"{winner} wins!", font=("Helvetica", 24))
        winner_label.pack(padx=20, pady=20)
        
        # Optionally, add a button to close the application or start a new game
        close_button = tk.Button(winner_window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)

    def squarePosToCanvasPos(self, square_pos: tuple) -> None:
        x = (ord(square_pos[0]) - ord('a')) * self.square_size + self.square_size/2
        y = (8-square_pos[1]) * self.square_size + self.square_size/2
        return (x, y)

    def canvasPosToSquarePos(self, canvas_pos: tuple) -> None:
        x, y = canvas_pos
        file = chr(int(x/self.square_size) + ord('a'))
        rank = 8 - int(y/self.square_size)
        return (file, rank)

    def getAndDrawValidMoves(self, piece):
        self.valid_moves.clear()
        start_file, start_rank = self.canvasPosToSquarePos(self.piece_inital_position) 
        self.createSquare(start_file, start_rank, self.light_blue_highlight, tag="highlight")

        for move in piece.getValidMoves(self.board):
            file, rank = move.target_square.file, move.target_square.rank
            self.createSquare(file, rank, self.dark_blue_highlight, tag="highlight")
            self.valid_moves[(file, rank)] = move
        
        self.canvas.tag_raise("pieces")