from copy import deepcopy
from config import *
import rules


def get_color(piece):
    return 'white' if piece.isupper() else 'black'


class Model(dict):

    captured_pieces = {'white': [], 'black': []}
    player_turn = 'white'
    halfmove_clock = 0
    move_nr = 1
    history = []
    can_castle_short = {'white': True, 'black': True}
    can_castle_long = {'white': True, 'black': True}
    all_available_moves = {'white': [], 'black': []}

    def __init__(self, *arg, **kw):
        super(Model, self).__init__(*arg, **kw)
        for pos, value in START_POSITION.items():
            self[pos] = value

    def get_movetext(self, pos_from, pos_to, piece_dest):
        hit = 'x' if piece_dest else ''
        piece_name = self[pos_from].upper() if self[pos_from].lower() != 'p' else ''
        if piece_dest:
            piece_name = self[pos_from].upper() if self[pos_from].lower() != 'p' else pos_from[0]
        movetext = piece_name + hit + pos_to
        if self[pos_from].lower() not in ['r', 'n']:
            return movetext
        for pos, piece_abbr in self.items():
            if piece_abbr == self[pos_from] and pos != pos_from:
                piece = self.get_piece_at_position(pos)
                other_move_list = rules.moves_available(self, pos, piece['name'], piece['color'])
                if pos_to in other_move_list:
                    movetext = piece_name + pos_from[0] + hit + pos_to
                    if pos[0] == pos_from[0]:
                        movetext = piece_name + pos_from[1] + hit + pos_to
        return movetext

    def update_game_stats(self, pos_from, pos_to, type_of_move):
        piece = self.get_piece_at_position(pos_from)
        piece_name = piece['name']
        color = piece['color']
        enemy = 'white' if color == 'black' else 'black'
        is_attacking = pos_to in self.keys() or type_of_move == 'en_passant'
        piece_dest = None
        if type_of_move == 'en_passant':
            piece_dest = 'Pawn'
        elif is_attacking:
            piece_dest = PIECE_NAME[self[pos_to].upper()]
        if color == 'black':
            self.move_nr += 1
        self.halfmove_clock += 1
        if piece_name == 'Pawn':
            self.halfmove_clock = 0
        movetext = self.get_movetext(pos_from, pos_to, is_attacking)
        if is_attacking:
            self.captured_pieces[enemy].append(piece_dest)
            self.halfmove_clock = 0
        if type_of_move == 'castle_short':
            movetext = '0-0'
        if type_of_move == 'castle_long':
            movetext = '0-0-0'
        if type_of_move == 'en_passant':
            movetext = '{}x{}'.format(pos_from[0], pos_to)
        self.history.append(movetext)
        self.player_turn = enemy
        # Castling
        if piece_name == 'King':
            self.can_castle_short[color] = False
            self.can_castle_long[color] = False
        if piece_name == 'Rook':
            if pos_from[0] == 'h':
                self.can_castle_short[color] = False
            if pos_from[0] == 'a':
                self.can_castle_long[color] = False

    def move(self, pos_from, pos_to, type_of_move):
        if type_of_move == 'en_passant':
            captured_pawn_pos = pos_to[0] + pos_from[1]
            del self[captured_pawn_pos]
        row = pos_from[1]
        self[pos_to] = self.pop(pos_from, None)
        if type_of_move == 'castle_short':
            self['f{}'.format(row)] = self.pop('h{}'.format(row), None)
        if type_of_move == 'castle_long':
            self['d{}'.format(row)] = self.pop('a{}'.format(row), None)

    def get_type_of_move(self, pos_from, pos_to):
        piece = self.get_piece_at_position(pos_from)
        piece_name = piece['name']
        type_of_move = 'normal'
        # Check for castling
        if piece_name == 'King' and pos_from[0] == 'e' and pos_to[0] == 'g':
            type_of_move = 'castle_short'
        if piece_name == 'King' and pos_from[0] == 'e' and pos_to[0] == 'c':
            type_of_move = 'castle_long'
        # Check for en-passant
        if piece_name == 'Pawn' and pos_to not in self.keys() and pos_to[0] != pos_from[0]:
            type_of_move = 'en_passant'
        return type_of_move

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
        if pos not in self.keys():
            return []
        piece = self.get_piece_at_position(pos)
        moves = rules.moves_available(self, pos, piece['name'], piece['color'])
        return moves

    def get_all_available_moves(self, color):
        result = []
        for pos in self.keys():
            piece = self.get_piece_at_position(pos)
            if piece['color'] == color:
                moves = self.get_available_moves(pos)
                result.extend(moves)
        self.all_available_moves[color] = result
        return result

    def all_occupied_positions(self):
        return list(self.keys())

    def all_positions_occupied_by_color(self, color):
        occupied = []
        for pos, piece in self.items():
            if get_color(piece) == color:
                occupied.append(pos)
        return occupied

    def get_piece_at_position(self, pos):
        piece = None
        if pos in self.keys():
            piece = dict(name=PIECE_NAME[self[pos].upper()], color=get_color(self[pos]))
        return piece
