import math
import pygame
import random


def inverse_gravity(x, y, center_x, center_y, strength=4.0):
    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    if distance == 0:
        return 0, 0  # No movement if at center

    force = strength / distance
    dx = (center_x - x) / distance * force
    dy = (center_y - y) / distance * force

    return dx, dy


def get_tangent_direction(x, y, center_x, center_y, speed=1.0):
    dx = x - center_x
    dy = y - center_y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance == 0:
        return 0, 0

    # Get unit tangent vector (perpendicular to radius)
    tangent_x = -dy / distance * speed
    tangent_y = dx / distance * speed

    return tangent_x, tangent_y

class Star:
    def __init__(self,x,y,dx,dy, radius, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color


class MenuBackground:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.center = self.width / 2, self.height / 2
        self.max_stars = 50
        self.current_stars = 0
        self.stars = []

    def run(self):
        if self.current_stars < self.max_stars:

            r = random.uniform(100, 255)
            g = random.uniform(100, 255)
            b = random.uniform(100, 255)

            star = Star(random.uniform(0, self.width), random.uniform(0, self.width), random.uniform(-1, 1),
                        random.uniform(-1, 1), random.uniform(1, 10), (r, g, b))
            star.dx, star.dy = get_tangent_direction(star.x, star.y, self.center[0], self.center[1], speed=2.0)
            self.stars.append(star)
            self.current_stars += 1

        self.draw_stars()
        stars_to_remove = []

        for star in self.stars:

            new_dx, new_dy = inverse_gravity(star.x, star.y, self.center[0], self.center[1])

            star.dx += new_dx
            star.dy += new_dy
            star.x += star.dx
            star.y += star.dy

            distance = math.sqrt((self.center[0] - star.x) ** 2) + ((self.center[1] - star.y) ** 2)

            if distance < 50:
                stars_to_remove.append(star)
            elif star.x < 0 or star.x > self.width:
                stars_to_remove.append(star)
            elif star.y < 0 or star.y > self.height:
                stars_to_remove.append(star)

        for star in stars_to_remove:
            self.stars.remove(star)
            self.current_stars -= 1

    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, star.color, (star.x, star.y), star.radius)


