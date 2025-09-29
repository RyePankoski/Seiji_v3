import pygame.display
from constants import *
from board import Board
from tray import Tray


class Client:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.board_rect = pygame.Rect(0, 0, LINE_LENGTH, LINE_LENGTH)
        self.board_rect.center = (int(self.width / 2), int(self.height / 2))
        self.board = Board(self.screen, self.board_rect)
        self.trays = []
        self.init_trays()

    def run(self, mouse_pos):
        if mouse_pos is not None:
            print(f"Clicked on board at {self.check_for_click_on_board(mouse_pos)}")
            print(f"Clicked on tray at {self.check_for_click_on_tray(mouse_pos)}")

        self.render_calls()

    def check_for_click_on_board(self, mouse_pos):
        return self.board.get_clicked_slot(*mouse_pos)

    def check_for_click_on_tray(self, mouse_pos):
        for tray in self.trays:
            slot = tray.get_clicked_slot(*mouse_pos)
            if slot:
                tray.selected_slot = slot
                return slot
            tray.selected_slot = None
        return None

    def init_trays(self):
        player_1_tray = Tray(
            self.board_rect.right + 20,  # x position (20 pixels right of board)
            self.board_rect.top,  # y position (aligned with top of board)
            600,
            400
        )

        player_2_tray = Tray(
            self.board_rect.right + 20,
            self.board_rect.bottom - 400,
            600,
            400,
        )

        self.trays.append(player_1_tray)
        self.trays.append(player_2_tray)

    def render_calls(self):
        self.board.draw()
        for tray in self.trays:
            tray.draw(self.screen)



