import pygame
from constants import *


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

        # Load textures for both players
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

    def run(self, mouse_pos):
        pass

    def draw(self):
        padding = 10
        pygame.draw.rect(self.screen, GRAY, (
            self.board_x - padding,
            self.board_y - padding,
            self.rect.width + padding * 2,
            self.rect.height + padding * 2
        ))
        self.screen.blit(self.board_surface, (self.board_x, self.board_y))

        # Draw pieces
        for (cell_x, cell_y), (piece_type, player) in self.pieces.items():
            # Calculate center position of the cell
            center_x = self.board_x + int(cell_x * self.cell_size + self.cell_size / 2)
            center_y = self.board_y + int(cell_y * self.cell_size + self.cell_size / 2)

            # Get and scale the appropriate texture based on player
            if player in self.piece_textures and piece_type in self.piece_textures[player]:
                texture = self.piece_textures[player][piece_type]
                piece_size = int(self.cell_size * 0.9)
                scaled_texture = pygame.transform.scale(texture, (piece_size, piece_size))
                texture_rect = scaled_texture.get_rect(center=(center_x, center_y))
                self.screen.blit(scaled_texture, texture_rect)

    def get_clicked_slot(self, mouse_x, mouse_y):
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return None

        rel_x = mouse_x - self.rect.x
        rel_y = mouse_y - self.rect.y

        cell_size = self.rect.width / (MAX_LINES - 1)
        col = int(rel_x / cell_size)
        row = int(rel_y / cell_size)

        return col, row

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
        pygame.draw.circle(self.board_surface, (75,75,75), center, interval / 2, 2)
        pygame.draw.circle(self.board_surface, (75,75,75), center, 10)

        pygame.draw.circle(self.board_surface, (75,75,75), center, interval/2 * 5, 1)
        pygame.draw.circle(self.board_surface, (75,75,75), center, interval / 2 * 9, 1)

        pygame.display.flip()