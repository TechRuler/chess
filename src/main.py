from tkinter import Tk, Frame, Label
from logic import Logic
class ChessBoard(Frame):
    def __init__(self, player1,player2,*arg, **kwarg):
        Frame.__init__(self, *arg, **kwarg)
        self.variables()
        self.setup_ui()
        self.logic = Logic(chessboard=self,player1=player1,player2=player2)

    def variables(self):
        self.brown = '#9E7B5A'
        self.white = '#F0D9B5'
        self.map = {}
        self.highlight_boxes = []
        self.selected_box = None
        self.pieces_dict = {
            'a1': '♖', 'b1': '♘', 'c1': '♗', 'd1': '♕', 'e1': '♔', 'f1': '♗', 'g1': '♘', 'h1': '♖',
            'a2': '♙', 'b2': '♙', 'c2': '♙', 'd2': '♙', 'e2': '♙', 'f2': '♙', 'g2': '♙', 'h2': '♙',
            'a7': '♟', 'b7': '♟', 'c7': '♟', 'd7': '♟', 'e7': '♟', 'f7': '♟', 'g7': '♟', 'h7': '♟',
            'a8': '♜', 'b8': '♞', 'c8': '♝', 'd8': '♛', 'e8': '♚', 'f8': '♝', 'g8': '♞', 'h8': '♜'
        }
        self.black_pieces = ['♟', '♜', '♞', '♝', '♛', '♚']
        self.white_pieces = ['♙', '♖', '♘', '♗', '♕', '♔']

    def setup_ui(self):
        rows = '12345678'
        columns = 'abcdefgh'
        for row_index, row in enumerate(rows):
            for column_index, col in enumerate(columns):
                coord = col + row
                color = self.brown if (row_index + column_index) % 2 == 0 else self.white
                box = Label(self, text='', anchor='center', bg=color, font=('Consolas', 30))
                box.grid(row=row_index, column=column_index, sticky='nsew')
                box.bind("<Button-1>", self.click)
                self.map[coord] = box
                if coord in self.pieces_dict.keys():
                    box.config(text=self.pieces_dict[coord])
                    
        for i in range(8):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

    def click(self, event):
        coord = self.get_key(target_value=event.widget, dict=self.map)
        box = event.widget
        # print(coord)
        if self.selected_box == box:
            self.clear_highlight()
            box.config(bg=self.reset_color(coord))
            self.selected_box = None
        else:
            # old_coord = ''
            if self.selected_box:
                old_coord = self.get_key(target_value=self.selected_box, dict=self.map)
                self.selected_box.config(bg=self.reset_color(old_coord))
            self.selected_box = box
            if self.selected_box.cget('bg')=='yellow':
                self.logic.movement(coord,old_coord)
            else:
                self.selected_box.config(bg='lightblue')
        self.clear_highlight()
        self.logic.check()
    def clear_highlight(self):
        for pos in self.highlight_boxes:
            box = self.map.get(pos)
            box.config(bg=self.reset_color(pos))
        self.highlight_boxes.clear()
    def highlight(self,pos):
        if pos not in self.highlight_boxes:
            box = self.map.get(pos)
            box.config(bg='yellow')
            self.highlight_boxes.append(pos)

    def get_key(self, target_value: str, dict: dict) -> str:
        for key, value in dict.items():
            if value == target_value:
                return key

    def reset_color(self, pos: str) -> str:
        col, row = pos[0], int(pos[1])
        return self.brown if ((ord(col) - ord('a') + 1) + row) % 2 == 0 else self.white


class Chess(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x700')
        self.title('Chess Game')
        

        self.player_1 = Label(self,text='Player 1',font=("Jetbrains Mono",15),anchor='w')
        self.player_2 = Label(self,text='Player 2',font=("Jetbrains Mono",15),anchor='w')
        self.chess_board = ChessBoard(master=self,player1=self.player_1,player2=self.player_2)

        self.player_1.pack(fill='x')
        self.chess_board.pack(expand='true', fill='both')
        self.player_2.pack(fill='x')


if __name__ == '__main__':
    game = Chess()
    game.mainloop()
