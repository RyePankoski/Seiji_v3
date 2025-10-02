import pygame
from Game.client import Client
from Top.menu import Menu


def handle_events(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return pygame.mouse.get_pos()
    return None


class GameManager:
    def __init__(self, screen):
        self.client = Client(screen)
        self.game_state = "menu"
        self.menu = Menu(screen)

    def run(self, events):
        mouse_pos = handle_events(events)
        if self.game_state == "menu":
            self.menu.run_menu(events)
            self.check_menu()
        elif self.game_state == "game":
            self.client.run(mouse_pos)

    def check_menu(self):
        if self.menu.return_state == "BEGIN":
            self.game_state = "game"
        if self.menu.return_state == "EXIT":
            pygame.quit()
