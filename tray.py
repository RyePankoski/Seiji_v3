import pygame
from constants import *


class Tray:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.cols = 5
        self.rows = 2

        self.selected_slot = None

        tray_texture = pygame.image.load('textures/piece_tray_texture.png')
        self.scaled_tray_texture = pygame.transform.scale(tray_texture, (width, height))
        tray_background_texture = pygame.image.load('textures/tray_background.png')
        self.scaled_tray_background_texture = pygame.transform.scale(tray_background_texture,(width + 10, height + 10))

    def draw(self, screen):
        self.surface.blit(self.scaled_tray_texture, (0, 0))
        padding = 40
        usable_width = self.rect.width - (2 * padding)
        usable_height = self.rect.height - (2 * padding)

        cell_width = usable_width / self.cols
        cell_height = usable_height / self.rows
        radius = int(min(cell_width, cell_height) * 0.45)

        for row in range(self.rows):
            for col in range(self.cols):
                center_x = int(padding + col * cell_width + cell_width / 2)
                center_y = int(padding + row * cell_height + cell_height / 2)
                pygame.draw.circle(self.surface, BLACK, (center_x, center_y), radius)

        if self.selected_slot:
            row, col = self.selected_slot
            center_x = int(padding + col * cell_width + cell_width / 2)
            center_y = int(padding + row * cell_height + cell_height / 2)
            pygame.draw.circle(self.surface, CYAN, (center_x, center_y), radius, 2)

        screen.blit(self.scaled_tray_background_texture, (self.rect.x - 5, self.rect.y - 5))
        screen.blit(self.surface, self.rect.topleft)

    def get_clicked_slot(self, mouse_x, mouse_y):
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return None

        rel_x = mouse_x - self.rect.x
        rel_y = mouse_y - self.rect.y

        cell_width = self.rect.width / self.cols
        cell_height = self.rect.height / self.rows

        col = int(rel_x / cell_width)
        row = int(rel_y / cell_height)

        return row, col