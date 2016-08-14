from config import *
import model


def get_text_position(column, row):
    x = X_AXIS_LABELS[column]
    y = Y_AXIS_LABELS[row]
    return '{}{}'.format(x, y)


def get_numeric_position(pos):
    x = X_AXIS_LABELS.index(pos[0])
    y = int(pos[1]) - 1
    return x, y


def get_clicked_position(event):
    col_size = row_size = DIMENSION_OF_SQUARES
    clicked_column = event.x // col_size
    clicked_row = 7 - (event.y // row_size)
    return get_text_position(clicked_column, clicked_row)


class Controller:

    def __init__(self):
        self.view = None
        self.model = model.Model()

    def on_square_clicked(self, event):
        selected_piece_pos = self.view.selected_piece_position
        position = get_clicked_position(event)
        is_new_piece = position in self.model.all_positions_occupied_by_color(self.model.player_turn)
        available_moves = self.model.get_available_moves(position if is_new_piece else selected_piece_pos)
        piece = self.model.get_piece_at_position(position if is_new_piece else selected_piece_pos)

        if is_new_piece:
            self.view.reset_highlight_list()
            available_moves = self.filter_check_moves(position, available_moves)
            if piece and piece['color'] == self.model.player_turn and available_moves:
                self.view.selected_piece_position = position
                self.view.update_highlight_list(available_moves)
        else:
            available_moves = self.filter_check_moves(selected_piece_pos, available_moves)
            if position in available_moves:
                self.make_move(selected_piece_pos, position, piece)
                norwegian_color = 'hvit' if piece['color'] == 'black' else 'sort'
                self.view.update_bottom_label('Det er {} sin tur'.format(norwegian_color))
                self.produce_all_available_moves()
            else:
                self.view.reset_highlight_list()
                self.view.selected_piece_position = None

    def filter_check_moves(self, pos, moves):
        copy_of_moves = moves[:]
        for move in moves:
            if self.model.will_move_cause_check(pos, move):
                copy_of_moves.remove(move)
        return copy_of_moves

    def make_move(self, pos_from, pos_to, piece):
        # type_of_move = 'normal', 'castle_short', 'castle_long', 'en_passant'
        type_of_move = self.model.get_type_of_move(pos_from, pos_to)
        self.model.update_game_stats(pos_from, pos_to, type_of_move)
        self.model.move(pos_from, pos_to, type_of_move)
        self.view.make_move(pos_from, pos_to, piece, type_of_move)
        self.view.update_move_history(self.model.move_nr, piece['color'], self.model.history[-1])
        self.view.reset_board_state()

    def produce_all_available_moves(self):
        self.model.get_all_available_moves('white')
        self.model.get_all_available_moves('black')

    def start_new_game(self, view):
        self.view = view
        self.view.reset_chessboard()
        self.model = model.Model()
