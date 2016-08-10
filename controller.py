from config import *


def get_text_position(column, row):
    x = X_AXIS_LABELS[column]
    y = Y_AXIS_LABELS[row]
    return '{}{}'.format(x, y)


def get_numeric_position(pos):
    x = X_AXIS_LABELS.index(pos[0])
    y = int(pos[1]) - 1
    return x, y


def get_piece_at_position(pos):
    if pos in START_POSITION.keys():
        return START_POSITION[pos]
    else:
        return None


def on_square_clicked(view, event):
    col_size = row_size = DIMENSION_OF_SQUARES
    clicked_column = event.x // col_size
    clicked_row = 7 - (event.y // row_size)
    position = get_text_position(clicked_column, clicked_row)
    if view.selected_piece_position:
        view.make_move(view.selected_piece_position, position)
    else:
        if get_piece_at_position(position):
            view.selected_piece_position = position
        else:
            view.reset_board_state()


def start_new_game(view):
    view.draw_all_pieces(START_POSITION)
    view.make_move('e2', 'e4')
