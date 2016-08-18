from config import *
import model
import promote


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
                norwegian_color_turn = 'hvit' if self.model.player_turn == 'white' else 'sort'
                self.view.update_bottom_label('Det er {} sin tur'.format(norwegian_color_turn))
                self.produce_all_available_moves()
                if self.check_for_mate():
                    player_won = 'white' if self.model.player_turn == 'black' else 'black'
                    norwegian_color_won = 'hvit' if self.model.player_turn == 'black' else 'sort'
                    self.view.update_bottom_label('Sjakk matt! Det er {} som har vunnet.'.format(norwegian_color_won))
                    self.view.add_mate_to_move_history(player_won)
                    return
                if self.check_for_stalemate():
                    self.view.update_bottom_label('Patt! Partiet endte med remis.')
                    self.view.add_stalemate_to_move_history()
                    return
                if self.model.is_king_under_check(self.model.player_turn):
                    self.view.add_check_to_move_history()
            else:
                self.view.reset_board_state()

    def filter_check_moves(self, pos, moves):
        copy_of_moves = moves[:]
        for move in moves:
            if self.model.will_move_cause_check(pos, move):
                copy_of_moves.remove(move)
        return copy_of_moves

    def make_move(self, pos_from, pos_to, piece):
        # type_of_move = 'normal', 'castle_short', 'castle_long', 'en_passant', 'promoting'
        type_of_move = self.model.get_type_of_move(pos_from, pos_to)
        if type_of_move == 'promoting':
            promote.PromoteDialog(self.view.canvas, piece['color'], pos_from, pos_to, self)
            return
        self.model.update_game_stats(pos_from, pos_to, type_of_move)
        self.model.move(pos_from, pos_to, type_of_move)
        self.view.make_move(pos_from, pos_to, piece, type_of_move)
        self.view.update_move_history(self.model.move_nr, piece['color'], self.model.history[-1])
        if self.model.captured_pieces['white'] or self.model.captured_pieces['black']:
            self.view.create_captured_pieces(self.model.captured_pieces)
        self.view.reset_board_state()

    def make_promotion_move(self, pos_from, pos_to, piece, color, choosing_view):
        choosing_view.destroy_choosing_view()
        self.model.update_game_stats(pos_from, pos_to, 'promoting', piece)
        self.model.do_promotion_move(pos_from, pos_to, piece)
        self.view.make_move(pos_from, pos_to, {'name': 'Pawn', 'color': color}, 'promoting', piece)
        self.view.update_move_history(self.model.move_nr, color, self.model.history[-1])
        if self.model.captured_pieces['white'] or self.model.captured_pieces['black']:
            self.view.create_captured_pieces(self.model.captured_pieces)
        self.view.reset_board_state()
        self.view.canvas.bind('<Button-1>', self.on_square_clicked)
        norwegian_color_turn = 'hvit' if self.model.player_turn == 'white' else 'sort'
        self.view.update_bottom_label('Det er {} sin tur'.format(norwegian_color_turn))
        self.produce_all_available_moves()
        if self.check_for_mate():
            player_won = 'white' if self.model.player_turn == 'black' else 'black'
            norwegian_color_won = 'hvit' if self.model.player_turn == 'black' else 'sort'
            self.view.update_bottom_label('Sjakk matt! Det er {} som har vunnet.'.format(norwegian_color_won))
            self.view.add_mate_to_move_history(player_won)
            return
        if self.check_for_stalemate():
            self.view.update_bottom_label('Patt! Partiet endte med remis.')
            self.view.add_stalemate_to_move_history()
            return
        if self.model.is_king_under_check(self.model.player_turn):
            self.view.add_check_to_move_history()

    def produce_all_available_moves(self):
        all_white_moves = []
        white_pieces = self.model.all_positions_occupied_by_color('white')
        for pos in white_pieces:
            moves = self.model.get_available_moves(pos)
            white_moves_not_in_check = self.filter_check_moves(pos, moves)
            all_white_moves.extend(white_moves_not_in_check)

        all_black_moves = []
        black_pieces = self.model.all_positions_occupied_by_color('black')
        for pos in black_pieces:
            moves = self.model.get_available_moves(pos)
            black_moves_not_in_check = self.filter_check_moves(pos, moves)
            all_black_moves.extend(black_moves_not_in_check)

        self.model.all_available_moves['white'] = all_white_moves
        self.model.all_available_moves['black'] = all_black_moves

    def check_for_mate(self):
        color_of_in_mate = self.model.player_turn
        is_in_check = self.model.is_king_under_check(color_of_in_mate)
        can_move = self.model.all_available_moves[color_of_in_mate]
        return is_in_check and not can_move

    def check_for_stalemate(self):
        is_in_check = self.model.is_king_under_check(self.model.player_turn)
        can_move = self.model.all_available_moves[self.model.player_turn]
        return not is_in_check and not can_move

    def start_new_game(self, view):
        self.view = view
        self.view.reset_chessboard()
        self.model = model.Model()
