import cProfile
import pstats
import pygame
import sys
from game_manager import GameManager


pygame.init()
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
clock = pygame.time.Clock()
FPS = 30
game_manager = GameManager(screen)

def main():
    running = True
    while running:
        screen.fill((0, 0, 0))
        dt = clock.tick(FPS) / 1000
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
        game_manager.run(events)
        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    try:
        main()
    finally:
        pr.disable()
        stats = pstats.Stats(pr)
        stats.sort_stats('tottime')
        stats.print_stats(20)
