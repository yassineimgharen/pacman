import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
sys.stderr = open(os.devnull, "w")
import pygame
sys.stderr = sys.__stderr__

from src.config import load
from src.game.game import Game
from src.game.highscore import save_scores, add_score
from src.ui.renderer import draw
from src.ui.hud import draw_hud
from src.ui.menu import get_player_name, draw_main_menu

if len(sys.argv) != 2:
    print("Usage: python pac-man.py <config_file>")
    sys.exit(1)

config_file = sys.argv[1]
cfg = load(config_file)

game = Game(cfg)
pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

while True:
    if draw_main_menu(screen, game.scores) == "quit":
        break

    # reset game state for new game
    game = Game(cfg)
    running = True
    quit_early = False
    current_level = 0
    tick = 0
    paused = False

    while running and current_level < len(cfg["levels"]):
        level = game.start_level(current_level)
        level_running = True
        while level_running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                # keydown = key was pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        level.player.move(0, -1, level.maze)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        level.player.move(0, 1, level.maze)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        level.player.move(-1, 0, level.maze)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        level.player.move(1, 0, level.maze)
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_i:
                        level.player.invincible = not level.player.invincible
                    elif event.key == pygame.K_n:
                        current_level += 1
                        level_running = False
                    elif event.key == pygame.K_f:
                        for ghost in level.ghosts:
                            ghost.frozen = not ghost.frozen
                    elif event.key == pygame.K_l:
                        level.player.lives += 1
                    elif event.key == pygame.K_q:
                        running = False
                        level_running = False
                #  player closed the window = stop
                if event.type == pygame.QUIT:
                    running = False
                    level_running = False
                    quit_early = True
            if level.is_won():
                current_level += 1
                level_running = False
            elif level.is_lost():
                running = False
                level_running = False
            elif not paused:
                level.update(dt)
            tick += 1
            if not quit_early:
                draw(screen, level, tick)
                draw_hud(screen, level, current_level)
                pygame.display.flip()

    if quit_early:
        break

    won = current_level >= len(cfg["levels"])
    name = get_player_name(screen, game.player.score, won)
    game.scores = add_score(game.scores, name, game.player.score)
    save_scores(cfg["highscore_filename"], game.scores)

pygame.quit()
save_scores(cfg["highscore_filename"], game.scores)
