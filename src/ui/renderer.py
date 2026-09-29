import pygame
import math

CELL = 32
WALL_COLOR = (33, 33, 222)
BG_COLOR = (0, 0, 0)
PACGUM_COLOR = (255, 222, 173)
SUPER_PACGUM_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 255, 0)
GHOST_COLORS = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
FRIGHTENED_COLOR = (0, 0, 200)
DEAD_COLOR = (100, 100, 255)


def _draw_walls(screen, maze):
    for y in range(maze.height):
        for x in range(maze.width):
            rx, ry = x * CELL, y * CELL
            cell = maze.grid[y][x]
            if cell & 1:
                pygame.draw.line(screen, WALL_COLOR, (rx, ry), (rx + CELL, ry), 3)
            if cell & 2:
                pygame.draw.line(screen, WALL_COLOR, (rx + CELL, ry), (rx + CELL, ry + CELL), 3)
            if cell & 4:
                pygame.draw.line(screen, WALL_COLOR, (rx, ry + CELL), (rx + CELL, ry + CELL), 3)
            if cell & 8:
                pygame.draw.line(screen, WALL_COLOR, (rx, ry), (rx, ry + CELL), 3)


def _draw_player(screen, player, tick):
    cx = player.x * CELL + CELL // 2
    cy = player.y * CELL + CELL // 2
    r = CELL // 2 - 3
    mouth = abs(math.sin(tick * 0.1)) * 40
    start_angle = math.radians(mouth)
    end_angle = math.radians(360 - mouth)
    # direction offset
    angle_offset = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}.get((player.dx, player.dy), 0)
    start = math.radians(angle_offset) + start_angle
    end = math.radians(angle_offset) + end_angle
    points = [(cx, cy)]
    steps = 30
    for i in range(steps + 1):
        a = start + (end - start) * i / steps
        points.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    if len(points) > 2:
        pygame.draw.polygon(screen, PLAYER_COLOR, points)


def _draw_ghost(screen, ghost, index, tick):
    cx = ghost.x * CELL + CELL // 2
    cy = ghost.y * CELL + CELL // 2
    r = CELL // 2 - 3

    if ghost.state == "FRIGHTENED":
        # flash white when about to expire
        color = (255, 255, 255) if (int(ghost.frightened_timer) % 2 == 0 and ghost.frightened_timer < 3) else FRIGHTENED_COLOR
    elif ghost.state == "DEAD":
        color = DEAD_COLOR
    else:
        color = GHOST_COLORS[index % len(GHOST_COLORS)]

    # body
    body_rect = pygame.Rect(cx - r, cy - r, r * 2, r * 2)
    pygame.draw.ellipse(screen, color, body_rect)
    pygame.draw.rect(screen, color, (cx - r, cy, r * 2, r))

    # wavy bottom
    wave_points = []
    segments = 4
    for i in range(segments + 1):
        wx = cx - r + (2 * r * i // segments)
        wy = cy + r - (4 if i % 2 == 0 else 0)
        wave_points.append((wx, wy))
    wave_points.append((cx + r, cy))
    wave_points.append((cx - r, cy))
    pygame.draw.polygon(screen, color, wave_points)

    # eyes
    if ghost.state != "DEAD":
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 180)
        for ex in [cx - r // 3, cx + r // 3]:
            pygame.draw.circle(screen, eye_color, (ex, cy - r // 4), r // 4)
            pygame.draw.circle(screen, pupil_color, (ex + 1, cy - r // 4 + 1), r // 8)


def draw(screen, level, tick=0):
    screen.fill(BG_COLOR)
    _draw_walls(screen, level.maze)

    for (x, y) in level.pacgums:
        if level.maze.grid[y][x] == 15:
            continue
        cx, cy = x * CELL + CELL // 2, y * CELL + CELL // 2
        pygame.draw.circle(screen, PACGUM_COLOR, (cx, cy), 3)

    for (x, y) in level.super_pacgums:
        cx, cy = x * CELL + CELL // 2, y * CELL + CELL // 2
        pulse = int(4 + 3 * abs(math.sin(tick * 0.05)))
        pygame.draw.circle(screen, SUPER_PACGUM_COLOR, (cx, cy), pulse)

    for i, ghost in enumerate(level.ghosts):
        _draw_ghost(screen, ghost, i, tick)

    _draw_player(screen, level.player, tick)

    pygame.display.flip()
