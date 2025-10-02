import pygame
from Util.constants import *


class Tray:
    def __init__(self, x, y, width, height, player):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.player = player
        self.pieces_per_row = 5

        self.selected_slot = None

        tray_texture = pygame.image.load('./Textures/piece_tray_texture.png')
        self.scaled_tray_texture = pygame.transform.scale(tray_texture, (width, height))
        tray_background_texture = pygame.image.load('./Textures/tray_background.png')
        self.scaled_tray_background_texture = pygame.transform.scale(tray_background_texture, (width + 10, height + 10))

        if self.player == 1:
            self.piece_textures = {
                "monarch": pygame.image.load('./Textures/pieces/player1/monarch.png'),
                "advisor": pygame.image.load('./Textures/pieces/player1/advisor.png'),
                "soldier": pygame.image.load('./Textures/pieces/player1/soldier.png'),
                "palace": pygame.image.load('./Textures/pieces/player1/palace.png'),
                "spy": pygame.image.load('./Textures/pieces/player1/spy.png'),
            }
        else:
            self.piece_textures = {
                "monarch": pygame.image.load('./Textures/pieces/player2/monarch.png'),
                "advisor": pygame.image.load('./Textures/pieces/player2/advisor.png'),
                "soldier": pygame.image.load('./Textures/pieces/player2/soldier.png'),
                "palace": pygame.image.load('./Textures/pieces/player2/palace.png'),
                "spy": pygame.image.load('./Textures/pieces/player2/spy.png'),
            }

        self.pieces = ["monarch", "advisor", "advisor", "soldier", "soldier", "soldier", "soldier", "soldier", "palace",
                       "spy"]

    def draw(self, screen):
        self.surface.blit(self.scaled_tray_texture, (0, 0))
        padding = 40
        usable_width = self.rect.width - (2 * padding)

        cell_width = usable_width / self.pieces_per_row
        radius = int(min(cell_width, cell_width) * 0.45)
        piece_size = radius * 2

        for idx, piece in enumerate(self.pieces):
            row = idx // self.pieces_per_row
            col = idx % self.pieces_per_row

            if piece in self.piece_textures:
                center_x = int(padding + col * cell_width + cell_width / 2)
                center_y = int(padding + row * cell_width + cell_width / 2)

                texture = self.piece_textures[piece]
                scaled_texture = pygame.transform.scale(texture, (piece_size, piece_size))
                texture_rect = scaled_texture.get_rect(center=(center_x, center_y))
                self.surface.blit(scaled_texture, texture_rect)

        if self.selected_slot is not None:
            idx = self.selected_slot
            row = idx // self.pieces_per_row
            col = idx % self.pieces_per_row

            center_x = int(padding + col * cell_width + cell_width / 2)
            center_y = int(padding + row * cell_width + cell_width / 2)
            pygame.draw.circle(self.surface, CYAN, (center_x, center_y), radius, 2)

        screen.blit(self.scaled_tray_background_texture, (self.rect.x - 5, self.rect.y - 5))
        screen.blit(self.surface, self.rect.topleft)

    def get_clicked_slot(self, mouse_x, mouse_y):
        if not self.rect.collidepoint(mouse_x, mouse_y):
            self.selected_slot = None
            return None

        rel_x = mouse_x - self.rect.x
        rel_y = mouse_y - self.rect.y

        padding = 40
        usable_width = self.rect.width - (2 * padding)
        cell_width = usable_width / self.pieces_per_row

        # Adjust for padding
        grid_x = rel_x - padding
        grid_y = rel_y - padding

        if grid_x < 0 or grid_y < 0:
            self.selected_slot = None
            return None

        col = int(grid_x / cell_width)
        row = int(grid_y / cell_width)

        idx = row * self.pieces_per_row + col

        # Check if click is within valid piece range
        if idx < 0 or idx >= len(self.pieces):
            self.selected_slot = None
            return None

        self.selected_slot = idx
        selected_piece = self.pieces[idx]

        return selected_piece, self.player
