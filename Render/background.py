import random
from Util.constants import *

import pygame.display


class Star:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = 1


class Background:
    def __init__(self, screen):
        self.screen = screen
        self.max_stars = 200
        self.current_stars = 0
        self.stars = []
        self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.origin_x = self.screen.get_width() / 2
        self.origin_y = self.screen.get_height() / 2

    def run(self):
        speed = 2
        if self.current_stars < self.max_stars:

            self.current_stars += 1

            dx = random.uniform(-speed, speed)
            dy = random.uniform(-speed, speed)

            # if random.random() < 0.01:
            #     r, g, b = random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255)
            #     self.stars.append(Star(self.origin_x, self.origin_y, dx, dy, (r, g, b)))
            # else:

            r = random.uniform(100, 255)
            g = random.uniform(100, 255)
            b = random.uniform(100, 255)

            self.stars.append(Star(self.origin_x, self.origin_y, dx, dy, (r,g,b)))

        stars_to_remove = []
        for star in self.stars:
            star.x += star.dx
            star.y += star.dy
            star.radius += 0.005
            star.radius = min(5, star.radius)

            pygame.draw.circle(self.screen, star.color, (star.x, star.y), star.radius)

            if star.x > self.width or star.x < 0 or star.y > self.height or star.y < 0:
                stars_to_remove.append(star)

        for star in stars_to_remove:
            self.current_stars -= 1
            self.stars.remove(star)
