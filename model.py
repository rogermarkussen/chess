from copy import deepcopy
from config import *
import exceptions
import rules


def get_color(piece):
    return 'white' if piece.isupper() else 'black'


class Model(dict):

    captured_pieces = {'white': [], 'black': []}
    player_turn = 'white'
    halfmove_clock = 0
    move_nr = 1
    history = []
    can_castle = {'white': True, 'black': True}

    def __init__(self, *arg, **kw):
        super(Model, self).__init__(*arg, **kw)
        self.reset_game_data()

    def reset_game_data(self):
        self.clear()
        for pos, value in START_POSITION.items():
            self[pos] = value
        captured_pieces = {'white': [], 'black': []}
        player_turn = 'white'
        halfmove_clock = 0
        move_nr = 1
        history = []
        can_castle = {'white': True, 'black': True}

    def update_game_stats(self, piece, piece_dest, color, pos_from, pos_to):
        enemy = 'white' if color == 'black' else 'black'
        if color == 'black':
            self.move_nr += 1
        self.halfmove_clock += 1
        piece_name = piece.upper()
        if piece_name == 'P':
            piece_name = ''
            self.halfmove_clock = 0
        if not piece_dest:
            movetext = piece_name + pos_to
        else:
            self.captured_pieces[enemy].append(piece_dest)
            movetext = piece_name + 'x' + pos_to
            self.halfmove_clock = 0
        self.history.append(movetext)
        self.player_turn = enemy

    def move(self, pos_from, pos_to):
        self[pos_to] = self.pop(pos_from, None)

    def move_validation(self, pos_from, pos_to):
        piece = None
        if pos_from in self.keys():
            piece = self[pos_from]
            piece_name = PIECE_NAME[piece.upper()]
            color = get_color(self[pos_from])
        else:
            return False
        piece_at_destination = None
        norwegian_color = 'hvit' if color == 'white' else 'sort'
        norwegian_enemy_color = 'sort' if color == 'white' else 'hvit'
        if pos_to in self.keys():
            piece_at_destination = self[pos_to]
        if self.player_turn != color:
            raise exceptions.NotYourTurn('Det er ikke {} i trekket!'.format(norwegian_color))
        enemy = 'white' if color == 'black' else 'black'
        moves_available = rules.moves_available(self, pos_from, piece_name, color)
        if pos_to not in moves_available:
            raise exceptions.InvalidMove
        if self.get_all_available_moves(enemy):
            if self.will_move_cause_check(pos_from, pos_to):
                raise exceptions.Check
        if not moves_available and self.is_king_under_check(color):
            raise exceptions.CheckMate
        elif not moves_available:
            raise exceptions.Draw
        else:
            self.move(pos_from, pos_to)
            self.update_game_stats(piece, piece_at_destination, color, pos_from, pos_to)
            return True, piece, piece_at_destination, norwegian_enemy_color

    def will_move_cause_check(self, pos_from, pos_to):
        color = get_color(self[pos_from])
        tmp = deepcopy(self)
        tmp[pos_to] = tmp.pop(pos_from, None)
        return tmp.is_king_under_check(color)

    def is_king_under_check(self, color):
        king_pos = self.get_king_position(color)
        opponent = 'white' if color == 'black' else 'black'
        return king_pos in self.get_all_available_moves(opponent)

    def get_king_position(self, color):
        king = 'K' if color == 'white' else 'k'
        for pos, piece in self.items():
            if piece == king:
                return pos

    def get_available_moves(self, pos):
        if pos in self.keys():
            piece_name = PIECE_NAME[self[pos].upper()]
            piece_color = get_color(self[pos])
            return rules.moves_available(self, pos, piece_name, piece_color)

    def get_all_available_moves(self, color):
        result = []
        for pos, piece in self.items():
            piece_name = PIECE_NAME[self[pos].upper()]
            piece_color = get_color(self[pos])
            if piece_color == color:
                moves = rules.moves_available(self, pos, piece_name, piece_color)
                if moves:
                    result.extend(moves)
        return result

    def all_occupied_positions(self):
        return list(self.keys())

    def all_positions_occupied_by_color(self, color):
        occupied = []
        for pos, piece in self.items():
            if get_color(piece) == color:
                occupied.append(pos)
        return occupied
