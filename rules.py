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
        initial_row_position, direction, enemy = 1, 1, 'black'
    else:
        initial_row_position, direction, enemy = 6, -1, 'white'
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
    return allowed_moves
