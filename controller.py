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

    def on_square_clicked(self, event):
        col_size = row_size = DIMENSION_OF_SQUARES
        clicked_column = event.x // col_size
        clicked_row = 7 - (event.y // row_size)
        position = get_text_position(clicked_column, clicked_row)
        self.produce_all_available_moves()
        available_moves = self.model.get_available_moves(position)

        if not self.view.selected_piece_position:
            piece = self.model.get_piece_at_position(position)
            if piece and piece['color'] == self.model.player_turn and available_moves:
                self.view.selected_piece_position = position
                self.view.update_highlight_list(available_moves)
        else:
            en_passant = False
            try:
                is_validated, norwegian_color, en_passant =\
                    self.model.move_validation(self.view.selected_piece_position, position)
            except exceptions.ChessError as error:
                is_validated = False
                self.view.bottom_label['text'] = error.__class__.__name__
                self.view.reset_board_state()
            else:
                self.view.bottom_label['text'] = 'Det er {} sin tur'.format(norwegian_color)

            if is_validated:
                piece = self.model.get_piece_at_position(position)
                self.view.make_move(self.view.selected_piece_position, position, piece, en_passant)
                self.view.reset_highlight()
                self.view.update_move_history(self.model.move_nr, piece['color'], self.model.history[-1])
                if self.model.check_if_won():
                    self.view.bottom_label['text'] = self.model.check_if_won()
            else:
                self.view.reset_board_state()
                piece = self.model.get_piece_at_position(position)
                if piece and piece['color'] == self.model.player_turn and available_moves:
                    self.view.selected_piece_position = position
                    self.view.update_highlight_list(available_moves)

    def start_new_game(self, view):
        self.view = view
        self.view.draw_all_pieces(START_POSITION)
        self.view.reset_history()
        self.model = model.Model()

    def produce_all_available_moves(self):
        self.model.moves['white'] = self.model.get_all_available_moves('white')
        self.model.moves['black'] = self.model.get_all_available_moves('black')
