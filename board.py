import pygame
from constants import *
from sound_manager import SoundManager


class Board:
    def __init__(self, screen, board_rect):
        self.pieces = {}
        self.screen = screen
        self.rect = board_rect
        width, height = pygame.display.get_desktop_sizes()[0]
        self.board_x = width / 2 - board_rect.width / 2
        self.board_y = height / 2 - board_rect.height / 2
        self.rect.topleft = (self.board_x, self.board_y)
        self.cell_size = self.rect.width / (MAX_LINES - 1)
        self.board_surface = pygame.Surface((board_rect.width, board_rect.height))
        board_texture = pygame.image.load('textures/wood.png')
        self.scaled_board_texture = pygame.transform.scale(board_texture, self.board_surface.get_size())
        self.init_board_surface()
        self.piece_textures = None
        self.init_textures()

        self.selected_piece_on_board = None
        self.selected_tray_piece = None

    def draw(self):
        padding = 10
        pygame.draw.rect(self.screen, GRAY, (
            self.board_x - padding,
            self.board_y - padding,
            self.rect.width + padding * 2,
            self.rect.height + padding * 2
        ))
        self.screen.blit(self.board_surface, (self.board_x, self.board_y))

        # Draw all pieces
        for piece in self.pieces.values():
            if piece is None:
                continue

            # Calculate center position of the cell
            center_x = self.board_x + int(piece.cx * self.cell_size + self.cell_size / 2)
            center_y = self.board_y + int(piece.cy * self.cell_size + self.cell_size / 2)

            # Get and scale the appropriate texture based on player
            if piece.player in self.piece_textures and piece.piece_type in self.piece_textures[piece.player]:

                texture = self.piece_textures[piece.player][piece.piece_type]
                piece_size = int(self.cell_size * 0.9)
                scaled_texture = pygame.transform.scale(texture, (piece_size, piece_size))
                texture_rect = scaled_texture.get_rect(center=(center_x, center_y))
                self.screen.blit(scaled_texture, texture_rect)

                if piece.is_promoted:
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), piece_size / 2, 2)

        # Draw valid moves for selected piece
        if self.selected_piece_on_board is not None:
            piece = self.selected_piece_on_board
            valid_moves = self.get_valid_moves(piece)

            # Draw the valid moves
            for target_x, target_y in valid_moves:
                center_x = self.board_x + int(target_x * self.cell_size + self.cell_size / 2)
                center_y = self.board_y + int(target_y * self.cell_size + self.cell_size / 2)

                # Check if there's an enemy piece here (capture indicator)
                is_capture = ((target_x, target_y) in self.pieces and
                              self.pieces[(target_x, target_y)] is not None and
                              self.pieces[(target_x, target_y)].player != piece.player)

                surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                if is_capture:
                    # Red circle for capture moves
                    pygame.draw.circle(surface, (200, 100, 100, 120),
                                       (int(self.cell_size / 2), int(self.cell_size / 2)),
                                       int(self.cell_size * 0.35))
                else:
                    # Green circle for regular moves
                    pygame.draw.circle(surface, (100, 200, 100, 100),
                                       (int(self.cell_size / 2), int(self.cell_size / 2)),
                                       int(self.cell_size * 0.3))
                self.screen.blit(surface, (center_x - self.cell_size / 2, center_y - self.cell_size / 2))

            # Draw selection circle on the selected piece
            center_x = self.board_x + int(piece.cx * self.cell_size + self.cell_size / 2)
            center_y = self.board_y + int(piece.cy * self.cell_size + self.cell_size / 2)
            pygame.draw.circle(self.screen, GOLD, (center_x, center_y), int(self.cell_size * 0.525), 2)

    def get_valid_moves(self, piece):
        valid_moves = []

        for dx, dy, max_dist in piece.get_move_directions():
            for step in range(1, max_dist + 1 if max_dist != float("inf") else MAX_LINES):
                target_x = piece.cx + dx * step
                target_y = piece.cy + dy * step

                if not (0 <= target_x < MAX_LINES - 1 and 0 <= target_y < MAX_LINES - 1):
                    break

                if (target_x, target_y) in self.pieces and self.pieces[(target_x, target_y)]:
                    blocking_piece = self.pieces[(target_x, target_y)]
                    if blocking_piece.player != piece.player:
                        valid_moves.append((target_x, target_y))
                    break
                else:
                    valid_moves.append((target_x, target_y))

        return valid_moves

    def get_clicked_slot(self, mouse_x, mouse_y):
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return None

        rel_x = mouse_x - self.rect.x
        rel_y = mouse_y - self.rect.y

        cell_size = self.rect.width / (MAX_LINES - 1)
        col = int(rel_x / cell_size)
        row = int(rel_y / cell_size)

        return col, row

    def check_for_promotions(self):
        for piece in self.pieces.values():
            adjacent_pieces = self.get_adjacent_pieces(piece)
            if len(adjacent_pieces) <= 0:
                piece.is_promoted = False
                piece.promoted_by = False
                continue

            for other_piece in adjacent_pieces:
                if piece == other_piece:
                    continue
                if piece.player != other_piece.player:
                    continue

                if piece.piece_type == "soldier" and other_piece.piece_type == "monarch":
                    if not piece.is_promoted:
                        piece.is_promoted = True
                        piece.promoted_by = "monarch"
                        SoundManager.play_sound("promote")

    def get_adjacent_pieces(self, piece):
        adjacent_pieces = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            if (dx + piece.cx, dy + piece.cy) in self.pieces:
                if self.pieces[(dx + piece.cx, dy + piece.cy)] is not None:
                    other_piece = self.pieces[(dx + piece.cx, dy + piece.cy)]

                    if piece.player == other_piece.player:
                        adjacent_pieces.append(other_piece)

        return adjacent_pieces


    def init_board_surface(self):
        self.board_surface.blit(self.scaled_board_texture, (0, 0))

        interval = self.board_surface.get_width() / (MAX_LINES - 1)
        xk = 0
        yk = 0

        for i in range(MAX_LINES):
            pygame.draw.line(self.board_surface, BLACK, (xk, 0), (xk, LINE_LENGTH), 2)
            xk += interval

        for i in range(MAX_LINES):
            pygame.draw.line(self.board_surface, BLACK, (0, yk), (LINE_LENGTH, yk), 2)
            yk += interval

        center = self.board_surface.get_rect().center
        pygame.draw.circle(self.board_surface, (75, 75, 75), center, interval / 2, 2)
        pygame.draw.circle(self.board_surface, (75, 75, 75), center, 10)

        pygame.draw.circle(self.board_surface, (75, 75, 75), center, interval / 2 * 5, 1)
        pygame.draw.circle(self.board_surface, (75, 75, 75), center, interval / 2 * 9, 1)

        pygame.display.flip()

    def init_textures(self):
        self.piece_textures = {
            1: {
                "monarch": pygame.image.load('textures/pieces/player1/monarch.png'),
                "advisor": pygame.image.load('textures/pieces/player1/advisor.png'),
                "soldier": pygame.image.load('textures/pieces/player1/soldier.png'),
                "palace": pygame.image.load('textures/pieces/player1/palace.png'),
                "spy": pygame.image.load('textures/pieces/player1/spy.png'),
            },
            2: {
                "monarch": pygame.image.load('textures/pieces/player2/monarch.png'),
                "advisor": pygame.image.load('textures/pieces/player2/advisor.png'),
                "soldier": pygame.image.load('textures/pieces/player2/soldier.png'),
                "palace": pygame.image.load('textures/pieces/player2/palace.png'),
                "spy": pygame.image.load('textures/pieces/player2/spy.png'),
            }
        }
