NR_OF_ROWS = 8
NR_OF_COLUMNS = 8
DIMENSION_OF_SQUARES = 81
COLOR_DARK = '#DDB88C'
COLOR_LIGHT = '#A66D4F'
COLOR_HIGHLIGHT = '#46B004'

X_AXIS_LABELS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
Y_AXIS_LABELS = (1, 2, 3, 4, 5, 6, 7, 8)

PIECE_NAME = {
    'R': 'Rook', 'N': 'Knight', 'B': 'Bishop',
    'Q': 'Queen', 'K': 'King', 'P': 'Pawn'
}

START_POSITION = {
    "a8": "r", "b8": "n", "c8": "b", "d8": "q", "e8": "k", "f8": "b", "g8": "n", "h8": "r",
    "a7": "p", "b7": "p", "c7": "p", "d7": "p", "e7": "p", "f7": "p", "g7": "p", "h7": "p",
    "a2": "P", "b2": "P", "c2": "P", "d2": "P", "e2": "P", "f2": "P", "g2": "P", "h2": "P",
    "a1": "R", "b1": "N", "c1": "B", "d1": "Q", "e1": "K", "f1": "B", "g1": "N", "h1": "R"
}

ORTHOGONAL_POSITIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
DIAGONAL_POSITIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
KNIGHT_POSITIONS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1))
