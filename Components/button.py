import pygame
from Util.constants import *


class Button:
    def __init__(self, x, y, width, height, screen, text='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.clicked = False
        self.mouse_over = False

        self.font = pygame.font.Font("./Fonts/main_font.ttf", 36)


    def run(self, events):
        self.handle_click(events)
        self.draw()

        if self.clicked:
            return True
        else:
            return False


    def handle_click(self, events):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_over = True
        else:
            self.mouse_over = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.clicked = True
                    else:
                        self.clicked = False

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, (self.rect.x - 2, self.rect.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(self.screen, BLACK, self.rect)

        if self.mouse_over:
            pygame.draw.rect(self.screen, (20,20,20), self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.x + self.width/2, self.rect.y + self.height/2))
        self.screen.blit(text_surface, text_rect)


