import pygame


def draw_hud(screen, level):
    font = pygame.font.SysFont(None, 36)
    w, _ = screen.get_size()
    score = font.render(f"Score: {level.player.score}", True, (255, 255, 255))
    lives = font.render(f"Lives: {level.player.lives}", True, (255, 255, 0))
    timer = font.render(f"Time: {int(level.timer)}", True, (255, 100, 100))
    screen.blit(score, (10, 10))
    screen.blit(lives, (w // 2 - lives.get_width() // 2, 10))
    screen.blit(timer, (w - timer.get_width() - 10, 10))
