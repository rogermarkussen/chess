from tkinter import *
from config import *
import controller as contr


def calc_piece_coordinate(pos):
    x0 = (pos[0] * DIMENSION_OF_SQUARES) + (DIMENSION_OF_SQUARES // 2)
    y0 = ((7 - pos[1]) * DIMENSION_OF_SQUARES) + (DIMENSION_OF_SQUARES // 2)
    return x0, y0


class View:

    canvas = None
    moves_display = None
    bottom_label = None
    selected_piece_position = None
    highlighted_squares = []
    images = {}
    color_dark = COLOR_DARK
    color_light = COLOR_LIGHT
    color_highlight = COLOR_HIGHLIGHT

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.__create_visual()
        self.canvas.bind('<Button-1>', self.controller.on_square_clicked)
        self.controller.start_new_game(self)

    def __create_visual(self):
        self.__create_menu()
        self.__create_canvas()
        self.__draw_board()
        self.__create_bottom_label()
        self.__create_move_display()

    def __create_menu(self):
        menu_bar = Menu(self.parent)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Nytt spill', command=lambda: self.controller.start_new_game(self))
        menu_bar.add_cascade(label='Fil', menu=file_menu)
        self.parent.config(menu=menu_bar)

    def __create_canvas(self):
        width = NR_OF_COLUMNS * DIMENSION_OF_SQUARES
        height = NR_OF_ROWS * DIMENSION_OF_SQUARES
        self.canvas = Canvas(self.parent, width=width, height=height)
        self.canvas.grid(row=0, column=0, rowspan=25, padx=4, pady=4)

    def __draw_board(self):
        active_color = self.color_dark
        for row in range(NR_OF_ROWS):
            active_color = self.__change_color(active_color)
            for col in range(NR_OF_COLUMNS):
                position = contr.get_text_position(col, row)
                x_top_left = col * DIMENSION_OF_SQUARES
                y_top_left = (7 - row) * DIMENSION_OF_SQUARES
                x_bottom_right = x_top_left + DIMENSION_OF_SQUARES
                y_bottom_right = y_top_left + DIMENSION_OF_SQUARES
                self.canvas.create_rectangle(x_top_left, y_top_left, x_bottom_right, y_bottom_right,
                                             fill=active_color, tags=('square-{}'.format(position), active_color))
                active_color = self.__change_color(active_color)

    def __create_bottom_label(self):
        self.bottom_label = Label(self.parent, text='Hvit skal starte spillet', font=('Arial', 15))
        self.bottom_label.grid(row=25, column=0, padx=10, pady=10)

    def __create_move_display(self):
        Label(self.parent, text='Utførte trekk', font=('Arial', 18)).grid(row=0, column=1, sticky=S)
        frame = Frame(self.parent, height=10, width=24)
        self.moves_display = Text(
            frame, padx=10, pady=10, height=10, width=24, spacing3=4, tabs=50,
            state=DISABLED)
        self.moves_display.pack(side=LEFT, fill=Y)
        frame.grid(row=1, column=1, padx=50, pady=0, sticky=N)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.moves_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.moves_display.yview)

    def __draw_highlight_square(self, pos):
        self.canvas.itemconfig('square-{}'.format(pos), fill=self.color_highlight)

    def __change_color(self, color):
        return self.color_light if color == self.color_dark else self.color_dark

    def __draw_single_piece(self, pos, piece):
        color = 'white' if piece.isupper() else 'black'
        piece_name = PIECE_NAME[piece.upper()].lower()
        filename = './pieces_image/{}_{}.png'.format(piece_name, color)
        if filename not in self.images:
            self.images[filename] = PhotoImage(file=filename)
        x0, y0 = calc_piece_coordinate(contr.get_numeric_position(pos))
        self.canvas.create_image(x0, y0, image=self.images[filename], tags=('occupied', pos), anchor='c')

    def draw_all_pieces(self, board_model):
        self.canvas.delete('occupied')
        for pos, piece in board_model.items():
            self.__draw_single_piece(pos, piece)

    def make_move(self, pos_from, pos_to, piece, type_of_move, promoting_piece=''):
        if pos_to not in self.highlighted_squares:
            return
        row = pos_from[1]
        piece_abbr = piece['name'][0].upper() if piece['name'] != 'Knight' else 'N'
        if piece['color'] == 'black':
            piece_abbr = piece_abbr.lower()
        if type_of_move == 'promoting':
            piece_abbr = promoting_piece
        self.canvas.delete(pos_from)
        self.canvas.delete(pos_to)
        self.__draw_single_piece(pos_to, piece_abbr)
        self.selected_piece_position = None
        if type_of_move == 'en_passant':
            captured_pawn_pos = pos_to[0] + pos_from[1]
            self.canvas.delete(captured_pawn_pos)
        rook_piece = {'name': 'Rook', 'color': piece['color']}
        if type_of_move == 'castle_short':
            self.make_move('h{}'.format(row), 'f{}'.format(row), rook_piece, '')
        if type_of_move == 'castle_long':
            self.make_move('a{}'.format(row), 'd{}'.format(row), rook_piece, '')

    def update_highlight_list(self, highlight_list):
        self.highlighted_squares = highlight_list
        for pos in highlight_list:
            self.__draw_highlight_square(pos)

    def reset_highlight_list(self):
        self.canvas.itemconfig(self.color_dark, fill=self.color_dark)
        self.canvas.itemconfig(self.color_light, fill=self.color_light)
        self.highlighted_squares = []

    def update_move_history(self, move_nr, color, move):
        self.moves_display.config(state=NORMAL)
        if move_nr > 1 and color == 'white':
            self.moves_display.insert(INSERT, '\n')
        if color == 'white':
            self.moves_display.insert(INSERT, '{}. {}'.format(move_nr, move))
        if color == 'black':
            self.moves_display.insert(INSERT, '\t\t{}'.format(move))
        self.moves_display.config(state=DISABLED)
        self.moves_display.yview(END)

    def add_check_to_move_history(self):
        self.moves_display.config(state=NORMAL)
        self.moves_display.insert(INSERT, '+')
        self.moves_display.config(state=DISABLED)

    def add_mate_to_move_history(self, player_won):
        self.moves_display.config(state=NORMAL)
        result_text = '#(1-0)' if player_won == 'white' else '#(0-1)'
        self.moves_display.insert(INSERT, result_text)
        self.moves_display.config(state=DISABLED)

    def add_stalemate_to_move_history(self):
        self.moves_display.config(state=NORMAL)
        self.moves_display.insert(INSERT, '(=)')
        self.moves_display.config(state=DISABLED)

    def update_bottom_label(self, text):
        self.bottom_label['text'] = text

    def reset_move_history(self):
        self.moves_display.config(state=NORMAL)
        self.moves_display.delete(1.0, END)
        self.update_bottom_label('Hvit skal starte spillet')

    def reset_board_state(self):
        self.selected_piece_position = None
        self.reset_highlight_list()

    def reset_chessboard(self):
        self.reset_board_state()
        self.draw_all_pieces(START_POSITION)
        self.reset_move_history()
