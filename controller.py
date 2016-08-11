from config import *
import model
import exceptions


def get_text_position(column, row):
    x = X_AXIS_LABELS[column]
    y = Y_AXIS_LABELS[row]
    return '{}{}'.format(x, y)


def get_numeric_position(pos):
    x = X_AXIS_LABELS.index(pos[0])
    y = int(pos[1]) - 1
    return x, y


class Controller:

    def __init__(self):
        self.view = None
        self.model = model.Model()

    def get_piece_at_position(self, pos):
        if pos in self.model.keys():
            return self.model[pos]
        else:
            return None

    def on_square_clicked(self, event):
        col_size = row_size = DIMENSION_OF_SQUARES
        clicked_column = event.x // col_size
        clicked_row = 7 - (event.y // row_size)
        position = get_text_position(clicked_column, clicked_row)
        piece_from = None
        piece_to = None
        if self.view.selected_piece_position:
            is_validated = False
            try:
                is_validated, piece_from, piece_to, norwegian_color = self.model.move_validation(self.view.selected_piece_position, position)
            except exceptions.ChessError as error:
                self.view.bottom_label['text'] = error.__class__.__name__
                self.view.reset_board_state()
            else:
                self.view.bottom_label['text'] = 'Det er {} sin tur'.format(norwegian_color)
            if is_validated:
                self.view.make_move(self.view.selected_piece_position, position, piece_from, piece_to)
        else:
            if self.get_piece_at_position(position):
                self.view.selected_piece_position = position
                highlight_list = self.model.get_available_moves(position)
                self.view.update_highlight_list(self.model, highlight_list)
            else:
                self.view.reset_board_state()

    def start_new_game(self, view):
        self.view = view
        self.view.draw_all_pieces(START_POSITION)
