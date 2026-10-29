"""Main menu and name entry screens."""

import pygame
import re
from src.ui.hud import CONTROLS


def draw_main_menu(screen: pygame.Surface, scores: list) -> str:
    """Show the main menu until the player makes a choice.

    Displays the title, the top 10 highscores and the controls.

    Returns:
        "play" when ENTER is pressed, "quit" on Q or window close.
    """
    font = pygame.font.SysFont(None, 72)
    small = pygame.font.SysFont(None, 36)
    tiny = pygame.font.SysFont(None, 28)
    w, h = screen.get_size()
    while True:
        screen.fill((0, 0, 0))
        screen.blit(font.render("PAC-MAN", True,
                                (255, 255, 0)), (w // 2 - 120, 60))
        screen.blit(small.render("ENTER - Start Game", True,
                                 (255, 255, 255)), (w // 2 - 120, 180))
        screen.blit(small.render("Q     - Quit", True,
                                 (255, 255, 255)), (w // 2 - 120, 230))
        screen.blit(small.render("-- Top 10 Highscores --",
                                 True, (255, 255, 0)), (w // 2 - 150, 310))
        for i, entry in enumerate(scores[:10]):
            line = tiny.render(f"{i+1}. {entry['name']} - {entry['score']}",
                               True, (200, 200, 200))
            screen.blit(line, (w // 2 - 120, 350 + i * 30))
        for i, text in enumerate(CONTROLS):
            color = (255, 255, 0) if text.startswith("--") else (200, 200, 200)
            screen.blit(tiny.render(text, True, color),
                        (w - 280, 310 + i * 30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                elif event.key == pygame.K_q:
                    return "quit"


def get_player_name(screen: pygame.Surface, score: int,
                    won: bool) -> str:
    """Ask the player for a name at the end of a game.

    Only letters, digits and spaces are accepted, up to 10 characters.

    Returns:
        The entered name, or "Player" if it is empty.
    """
    font = pygame.font.SysFont(None, 72)
    small = pygame.font.SysFont(None, 36)
    w, h = screen.get_size()
    name = ""
    while True:
        screen.fill((0, 0, 0))
        title = font.render("YOU WIN!" if won else "GAME OVER",
                            True, (0, 255, 0) if won else (255, 0, 0))
        screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 120))
        screen.blit(small.render(f"Score: {score}", True,
                                 (255, 255, 255)), (w // 2 - 60, h // 2 - 50))
        screen.blit(small.render("Enter name:", True,
                                 (200, 200, 200)), (w // 2 - 70, h // 2 + 10))
        screen.blit(small.render(name + "_", True,
                                 (255, 255, 0)), (w // 2 - 60, h // 2 + 50))
        screen.blit(small.render("ENTER to confirm", True,
                                 (150, 150, 150)), (w // 2 - 90, h // 2 + 100))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return name.strip() or "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "Player"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10 and re.match(r"^[A-Za-z0-9 ]$",
                                                 event.unicode):
                    name += event.unicode
