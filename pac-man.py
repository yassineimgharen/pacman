import sys
from src.config import load
from src.game.game import Game
import pygame


if len(sys.argv) != 2:
    print("Usage: python pac-man.py <config_file>")
    sys.exit(1)

config_file = sys.argv[1]
cfg = load(config_file)
game = Game(cfg)
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
current_level = 0

while running and current_level < len(cfg["levels"]):
    level = game.start_level(current_level)
    level_running = True
    while level_running:
        dt = clock.tick(cfg["fps"]) / 1000
        for event in pygame.event.get():
            #  player closed the window = stop
            if event.type == pygame.QUIT:
                running = False
                level_running = False
        if level.is_won():
            current_level += 1
            # exit inner loop → outer loop creates next level
            level_running = False
        elif level.is_lost():
            running = False
            level_running = False
        else:
            level.update(dt)

pygame.quit()
