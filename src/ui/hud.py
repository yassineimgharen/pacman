import pygame

CONTROLS = [
    "-- Controls --",
    "Arrow / WASD: Move",
    "SPACE: Pause",
    "",
    "-- Cheat Keys --",
    "I: Invincibility",
    "F: Freeze ghosts",
    "L: Add life",
    "N: Skip level",
    "Q: Quit game",
]


def draw_hud(screen: object, level: object, current_level: int = 0) -> None:
    """Draw HUD with score, lives, timer and controls panel."""
    font = pygame.font.SysFont(None, 36)
    tiny = pygame.font.SysFont(None, 24)
    w, h = screen.get_size()
    score = font.render(f"Score: {level.player.score}", True, (255, 255, 255))
    lives = font.render(f"Lives: {level.player.lives}", True, (255, 255, 0))
    lvl = font.render(f"Level: {current_level + 1}", True, (100, 200, 255))
    timer = font.render(f"Time: {int(level.timer)}", True, (255, 100, 100))
    screen.blit(score, (10, 10))
    screen.blit(lives, (w // 4, 10))
    screen.blit(lvl, (w // 2 - lvl.get_width() // 2, 10))
    screen.blit(timer, (w - timer.get_width() - 10, 10))

    from src.ui.renderer import HUD_HEIGHT, _cell  # noqa: E402
    cell = _cell(screen, level.maze)
    maze_w = level.maze.width * cell
    panel_x = maze_w + 10
    if panel_x + 50 < w:
        for i, line in enumerate(CONTROLS):
            color = (255, 255, 0) if line.startswith("--") else (200, 200, 200)
            screen.blit(tiny.render(line, True, color),
                        (panel_x, HUD_HEIGHT + 10 + i * 22))
