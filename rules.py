import controller as contr
from config import *


def is_on_board(col, row):
    return 0 <= row <= 7 and 0 <= col <= 7


def get_directions_and_distance(piece):
    directions = None
    distance = 0
    if piece == 'King':
        directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
        distance = 1
    if piece == 'Queen':
        directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
        distance = 8
    if piece == 'Rook':
        directions = ORTHOGONAL_POSITIONS
        distance = 8
    if piece == 'Bishop':
        directions = DIAGONAL_POSITIONS
        distance = 8
    return directions, distance


def moves_available(model, pos, piece, color):
    if piece == 'Knight':
        return knight_moves(model, pos, color)
    if piece == 'Pawn':
        return pawn_moves(model, pos, color)
    if piece == 'King':
        return king_moves(model, pos, color)
    allowed_moves = []
    directions, distance = get_directions_and_distance(piece)
    start_col, start_row = contr.get_numeric_position(pos)
    for x, y in directions:
        collision = False
        for step in range(1, distance + 1):
            num_dest = start_col + step * x, start_row + step * y
            if collision or not is_on_board(*num_dest):
                break
            destination = contr.get_text_position(*num_dest)
            if destination not in model.keys():
                allowed_moves.append(destination)
            elif destination in model.all_positions_occupied_by_color(color):
                collision = True
            else:
                allowed_moves.append(destination)
                collision = True
    return allowed_moves


def knight_moves(model, pos, color):
    allowed_moves = []
    start_col, start_row = contr.get_numeric_position(pos)
    for x, y in KNIGHT_POSITIONS:
        num_dest = start_col + x, start_row + y
        if not is_on_board(*num_dest):
            continue
        destination = contr.get_text_position(*num_dest)
        if destination not in model.all_positions_occupied_by_color(color):
            allowed_moves.append(destination)
    return allowed_moves


def pawn_moves(model, pos, color):
    allowed_moves = []
    start_col, start_row = contr.get_numeric_position(pos)
    if color == 'white':
        initial_row_position, direction, enemy, en_passant_row = 1, 1, 'black', 4
    else:
        initial_row_position, direction, enemy, en_passant_row = 6, -1, 'white', 3
    # Moving forward
    forbidden = model.all_occupied_positions()
    num_dest = start_col, start_row + direction
    destination = contr.get_text_position(*num_dest)
    if destination not in forbidden:
        allowed_moves.append(destination)
        if start_row == initial_row_position:
            num_dest2 = start_col, start_row + direction * 2
            destination2 = contr.get_text_position(*num_dest2)
            if destination2 not in forbidden:
                allowed_moves.append(destination2)
    # Attacking
    for a in range(-1, 2, 2):
        num_dest_attack = start_col + a, start_row + direction
        if not is_on_board(*num_dest_attack):
            continue
        destination_attack = contr.get_text_position(*num_dest_attack)
        if destination_attack in model.all_positions_occupied_by_color(enemy):
            allowed_moves.append(destination_attack)
    # En passant
    if start_row == en_passant_row:
        can_do_en_passant = ''
        enemy_pawn_on_side_and_free_pos_in_front = []
        for a in range(-1, 2, 2):
            side_position = (start_col + a, start_row)
            dest_position = (start_col + a, start_row + direction)
            if is_on_board(*side_position):
                text_side_position = contr.get_text_position(*side_position)
                text_dest_position = contr.get_text_position(*dest_position)
                if text_side_position in model.keys() and text_dest_position not in model.keys():
                    side_piece = model[text_side_position].lower()
                    side_color = 'white' if model[text_side_position].isupper() else 'black'
                    if side_piece == 'p' and side_color == enemy:
                        enemy_pawn_on_side_and_free_pos_in_front.append([text_side_position, text_dest_position])
        if not enemy_pawn_on_side_and_free_pos_in_front:
            return allowed_moves
        for entry in enemy_pawn_on_side_and_free_pos_in_front:
            if model.history[-1] == entry[0] and entry[1] not in model.history:
                allowed_moves.append(entry[1])
    return allowed_moves


def king_moves(model, pos, color):
    allowed_moves = []
    directions, distance = get_directions_and_distance('King')
    start_col, start_row = contr.get_numeric_position(pos)
    for x, y in directions:
        num_dest = start_col + x, start_row + y
        if not is_on_board(*num_dest):
            continue
        destination = contr.get_text_position(*num_dest)
        if destination not in model.all_positions_occupied_by_color(color):
            allowed_moves.append(destination)
    allowed_moves.extend(get_castle_moves(model, pos, color))
    return allowed_moves


def get_castle_moves(model, pos, color):
    castle_moves = []
    row = '1' if color == 'white' else '8'
    enemy = 'white' if color == 'black' else 'black'
    enemy_available_moves = model.moves[enemy]
    king_pos = 'e{}'.format(row)
    if pos != king_pos:
        return []
    if pos in enemy_available_moves:
        return []
    if model.can_castle_short[color]:
        short_castle = True
        active_squares = ['f{}'.format(row), 'g{}'.format(row)]
        for square in active_squares:
            if square in model.keys():
                short_castle = False
            if square in enemy_available_moves:
                short_castle = False
        if short_castle:
            castle_moves.append('g{}'.format(row))
    if model.can_castle_long[color]:
        long_castle = True
        active_squares = ['d{}'.format(row), 'c{}'.format(row)]
        for square in active_squares:
            if square in model.keys():
                long_castle = False
            if square in enemy_available_moves:
                long_castle = False
        if 'b{}'.format(row) in model.keys():
            long_castle = False
        if long_castle:
            castle_moves.append('c{}'.format(row))
    return castle_moves
