from tkinter import Frame 
from tkinter.messagebox import showinfo
class Logic:
    def __init__(self, player1:str,player2:str,chessboard: Frame):
        self.chessboard: Frame = chessboard
        self.count: int = 0
        self.player1 = player1
        self.player2 = player2
        self.player_1_name = 'Player 1'
        self.player_2_name = 'Player 2'
    def win(self,piece):
        if piece['text'] in self.chessboard.white_pieces:
            showinfo('Game Over','Contratulations! Player 2 win this game')
        elif piece['text'] in self.chessboard.black_pieces:
            showinfo('Game Over','Contratulations! Player 1 win this game')
        self.player_1_name = 'Player 1'
        self.player_2_name = 'Player 2'
        self.player1.config(text=self.player_1_name)
        self.player2.config(text=self.player_2_name)
        self.chessboard.variables()
        self.chessboard.setup_ui()
    def movement(self, pos, old_pos):
        if not old_pos:
            return
        self.count+=1
        #getting places
        new_box = self.chessboard.map.get(pos)
        old_box = self.chessboard.map.get(old_pos)
        #getting elemeneted pieces
        if new_box['text'] != '':
            self.get_elimented_piece(new_box['text'])
        #declaring winnerr
        if new_box['text'] in ['♔','♚']:
            self.win(new_box)

        #movement
        try:
            new_box['text'] = old_box['text']
            old_box['text'] = ''
        except Exception as e:
            print(f'Error:{e}')
        
        
        self.chessboard.pieces_dict[pos] = self.chessboard.pieces_dict.pop(old_pos)
        self.chessboard.selected_box = None

        self.chessboard.clear_highlight()
        
        
    def get_elimented_piece(self,piece):
        if piece in self.chessboard.white_pieces:
            self.player_2_name+=piece
            self.player2.config(text=self.player_2_name)
        elif piece in self.chessboard.black_pieces:
            self.player_1_name+=piece
            self.player1.config(text=self.player_1_name)
    def check(self):
        if not self.chessboard.selected_box:
            return  # No box is selected
        piece = self.chessboard.selected_box.cget('text')
        is_white_turn = self.count % 2 == 0

        # Validate turn and handle the piece
        if (is_white_turn and piece in self.chessboard.white_pieces) or \
           (not is_white_turn and piece in self.chessboard.black_pieces):
            self.handle_piece(piece, 'white' if is_white_turn else 'black')
        else:
            print("Invalid or not your turn!")

    def handle_piece(self, piece, group):
        piece_guide = {
            '♙': self.pawn_guide, '♟': self.pawn_guide,
            '♖': self.rook_guide, '♜': self.rook_guide,
            '♘': self.knight_guide, '♞': self.knight_guide,
            '♗': self.bishop_guide, '♝': self.bishop_guide,
            '♕': self.queen_guide, '♛': self.queen_guide,
            '♔': self.king_guide, '♚': self.king_guide,
        }
        if piece in piece_guide:
            piece_guide[piece](group)

    def is_same_group(self, pos):
        box = self.chessboard.map.get(pos)
        selected_piece = self.chessboard.selected_box.cget('text')
        return box and (
            (box.cget('text') in self.chessboard.white_pieces and selected_piece in self.chessboard.white_pieces) or
            (box.cget('text') in self.chessboard.black_pieces and selected_piece in self.chessboard.black_pieces)
        )
    def is_different_group(self,pos):
        box = self.chessboard.map.get(pos)
        selected_piece = self.chessboard.selected_box.cget('text')
        return box and (
            (box.cget('text') in self.chessboard.white_pieces and selected_piece in self.chessboard.black_pieces) or
            (box.cget('text') in self.chessboard.black_pieces and selected_piece in self.chessboard.white_pieces)
        )
    
    def show_path(self, pos):
        if not self.is_same_group(pos) and not self.is_different_group(pos):
            self.chessboard.highlight(pos)
            return True
        elif self.is_different_group(pos):
            self.chessboard.highlight(pos)
            return False
                
        return False 

    def pawn_guide(self, group):
        pos = self.chessboard.get_key(self.chessboard.selected_box, self.chessboard.map)
        col, row = pos[0], int(pos[1])
        direction = 1 if self.chessboard.selected_box.cget('text') in self.chessboard.white_pieces else -1
        start_row = 2 if self.chessboard.selected_box.cget('text') in self.chessboard.white_pieces else 7

        # Regular move
        if self.chessboard.map[f"{col}{row + direction}"].cget('text')=='' and 'a'<=col<='h':
            self.show_path(f"{col}{row + direction}")
            # Double move from starting position
            if row == start_row:
                self.show_path(f"{col}{row + 2 * direction}")
                
        
        crossLeft = f'{chr(ord(col)-1)}{row+direction}'
        crossRight = f'{chr(ord(col)+1)}{row+direction}'
        

        try:
            if self.chessboard.map[crossLeft].cget('text')!='' and 'a'<=col<='h':
                self.show_path(crossLeft)
        except Exception as e:
            pass
        try:
            if self.chessboard.map[crossRight].cget('text')!='' and 'a'<=col<='h':
                self.show_path(crossRight)
        except Exception as e:
            pass

    def rook_guide(self, group):
        self._guide_straight_lines()

    def knight_guide(self, group):
        self._guide_knight_moves()

    def bishop_guide(self, group):
        self._guide_diagonal_lines()

    def queen_guide(self, group):
        self._guide_straight_lines()
        self._guide_diagonal_lines()

    def king_guide(self, group):
        pos = self.chessboard.get_key(self.chessboard.selected_box, self.chessboard.map)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dx, dy in directions:
            new_col = chr(ord(pos[0]) + dx)
            new_row = str(int(pos[1]) + dy)
            if 'a' <= new_col <= 'h' and '1' <= new_row <= '8':
                self.show_path(new_col + new_row)
    def _guide_knight_moves(self):
        pos = self.chessboard.get_key(self.chessboard.selected_box, self.chessboard.map)
        col, row = pos[0], int(pos[1])
        moves = [
            (2, 1), (2, -1),  # Two steps horizontally, one step vertically
            (-2, 1), (-2, -1),  # Two steps horizontally in the other direction
            (1, 2), (1, -2),  # One step horizontally, two steps vertically
            (-1, 2), (-1, -2)  # One step horizontally in the other direction
        ]

        for dx, dy in moves:
            new_col = chr(ord(col) + dx)
            new_row = row + dy

            # Validate if the new position is within the board
            if 'a' <= new_col <= 'h' and 1 <= new_row <= 8:
                self.show_path(f"{new_col}{new_row}")

    def _guide_straight_lines(self):
        pos = self.chessboard.get_key(self.chessboard.selected_box, self.chessboard.map)
        col, row = pos[0], int(pos[1])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Up, down, right, left

        for dx, dy in directions:
            self._guide_in_direction(col, row, dx, dy)

    def _guide_diagonal_lines(self):
        pos = self.chessboard.get_key(self.chessboard.selected_box, self.chessboard.map)
        col, row = pos[0], int(pos[1])
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonals

        for dx, dy in directions:
            self._guide_in_direction(col, row, dx, dy)

    def _guide_in_direction(self, col, row, dx, dy):
        while True:
            row += dy
            col = chr(ord(col) + dx)
            if 'a' <= col <= 'h' and 1 <= row <= 8:
                if not self.show_path(f"{col}{row}"):
                    break
            else:
                break


