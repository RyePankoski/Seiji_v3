from Render.sound_manager import SoundManager
from Top.game_manager import GameManager
import cProfile
import pygame
import pstats
import sys

pygame.init()
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
game_manager = GameManager(screen)
clock = pygame.time.Clock()
FPS = 30


def main():
    running = True
    while running:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        clock.tick(FPS) / 1000
        for event in events:
            if event.type == pygame.QUIT:
                return False

        SoundManager.game_music()
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
