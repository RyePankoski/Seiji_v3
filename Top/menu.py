from Components.button import Button
import pygame
from Render.menu_background import MenuBackground
from Util.constants import *


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.buttons = []
        self.buttons_width = 400
        self.buttons_height = 100
        self.init_buttons()
        self.menu_background = MenuBackground(screen)
        self.return_state = None

        self.title_font = pygame.font.Font("./Fonts/title_font.otf", 200)
        self.title_text = self.title_font.render("Seiji", True, GOLD)
        self.title_rect = self.title_text.get_rect(center=(self.width/2, 200))



    def run_menu(self, events):
        self.menu_background.run()
        for button in self.buttons:
            button.run(events)
            if button.clicked:

                self.return_state = button.text
                print(f"{self.return_state}")

        self.screen.blit(self.title_text, self.title_rect)

    def init_buttons(self):
        button_offset = 150
        top_button = 400

        start_button = Button(self.width / 2 - self.buttons_width/2, top_button, self.buttons_width,
                              self.buttons_height,  self.screen, "BEGIN")
        host_button = Button(self.width / 2 - self.buttons_width/2,top_button + button_offset, self.buttons_width,
                             self.buttons_height,  self.screen, "HOST")
        join_button = Button(self.width / 2 - self.buttons_width/2, top_button + button_offset * 2, self.buttons_width,
                             self.buttons_height,  self.screen, "JOIN")
        options_button = Button(self.width / 2 - self.buttons_width/2, top_button + button_offset * 3, self.buttons_width,
                              self.buttons_height,  self.screen, "OPTIONS")
        credits_button = Button(self.width / 2 - self.buttons_width/2, top_button + button_offset * 4, self.buttons_width,
                                self.buttons_height,  self.screen, "CREDITS")
        quit_button = Button(self.width / 2 - self.buttons_width/2, top_button + button_offset * 5, self.buttons_width,
                              self.buttons_height,  self.screen, "EXIT")

        self.buttons = [start_button, host_button, join_button, options_button, credits_button, quit_button]