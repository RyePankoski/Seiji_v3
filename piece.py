class Piece:
    MOVE_PATTERNS = {
        'monarch': {
            'base': [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1)],  # Orthogonal, one step
            'promoted': [((0, 1), 2), ((0, -1), 2), ((1, 0), 2), ((-1, 0), 2),
                         ((1, 1), 2), ((1, -1), 2), ((-1, 1), 2), ((-1, -1), 2)]  # Orthogonal + diagonal, 2 steps
        },
        'soldier': {
            'base': [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1)],
            'promoted_by_monarch': [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1),
                                    ((1, 1), 1), ((1, -1), 1), ((-1, 1), 1), ((-1, -1), 1)],
            'promoted_by_advisor': [((0, 1), 2), ((0, -1), 2), ((1, 0), 2), ((-1, 0), 2)]
        },
        'advisor': {
            'base': [((1, 1), 3), ((1, -1), 3), ((-1, 1), 3), ((-1, -1), 3)],  # up to 3 steps diagonally
            'promoted_by_monarch': [((0, 1), 2), ((0, -1), 2), ((1, 0), 2), ((-1, 0), 2),
                                    ((1, 1), 2), ((1, -1), 2), ((-1, 1), 2), ((-1, -1), 2)]
        },
        'spy': {
            'base': [((0, 1), 1), ((0, -1), 1), ((1, 0), 1), ((-1, 0), 1),
                     ((1, 1), 1), ((1, -1), 1), ((-1, 1), 1), ((-1, -1), 1)]
        }
    }

    def __init__(self, cx, cy, piece_type, player):
        self.cx = cx
        self.cy = cy
        self.piece_type = piece_type
        self.player = player
        self.is_promoted = False
        self.promoted_by = None

    def get_move_directions(self):
        """Return directions as (dx, dy, max_dist)."""
        piece_data = self.MOVE_PATTERNS.get(self.piece_type, {})

        if self.promoted_by == 'monarch':
            move_type = 'promoted_by_monarch'
        elif self.promoted_by == 'advisor':
            move_type = 'promoted_by_advisor'
        elif self.is_promoted:
            move_type = 'promoted'
        else:
            move_type = 'base'

        return [(dx, dy, dist) for (dx, dy), dist in piece_data.get(move_type, [])]

    def promote(self, promoted_by_piece):
        self.is_promoted = True
        self.promoted_by = promoted_by_piece
