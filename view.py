from tkinter import *
from config import *
import controller


class View:

    canvas = None
    selected_piece_position = None
    highlighted_squares = []
    images = {}
    color_dark = COLOR_DARK
    color_light = COLOR_LIGHT
    color_highlight = COLOR_HIGHLIGHT

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        self.make_chess_board()

    def make_chess_board(self):
        self.make_canvas()
        active_color = self.color_dark
        for row in range(NR_OF_ROWS):
            active_color = self.change_color(active_color)
            for column in range(NR_OF_COLUMNS):
                x_top_left = column * DIMENSION_OF_FIELDS
                y_top_left = (7 - row) * DIMENSION_OF_FIELDS
                x_bottom_right = x_top_left + DIMENSION_OF_FIELDS
                y_bottom_right = y_top_left + DIMENSION_OF_FIELDS
                self.canvas.create_rectangle(x_top_left, y_top_left, x_bottom_right, y_bottom_right, fill=active_color)
                active_color = self.change_color(active_color)

    def make_canvas(self):
        width = NR_OF_COLUMNS * DIMENSION_OF_FIELDS
        height = NR_OF_ROWS * DIMENSION_OF_FIELDS
        self.canvas = Canvas(self.parent, width=width, height=height)
        self.canvas.pack(padx=8, pady=8)

    def change_color(self, color):
        return self.color_light if color == self.color_dark else self.color_dark


def main(model):
    root = Tk()
    root.title('Chess')
    View(root, model)
    root.mainloop()


def init_new_game():
    initial_game_data =controller.Controller()
    main(initial_game_data)


if __name__ == '__main__':
    init_new_game()
