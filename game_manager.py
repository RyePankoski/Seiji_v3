import pygame
from client import Client


def handle_events(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               return pygame.mouse.get_pos()
    return None


class GameManager:
    def __init__(self, screen):
        self.client = Client(screen)

    def run(self, events):
        mouse_pos = handle_events(events)
        self.client.run(mouse_pos)
