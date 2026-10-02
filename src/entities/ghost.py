from src.maze import Maze
from src.entities.player import Player
import random


class Ghost:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.home_x = x
        self.home_y = y
        self.state = "CHASE"
        self.frightened_timer = 0  # counts down when frightened
        self.dead_timer = 0  # counts down when dead
        self.frozen = False
        self.move_timer = 0
        self.last_dx = 0
        self.last_dy = 0
        self.rx = float(x)
        self.ry = float(y)

    def frighten(self, duration: int):
        self.state = "FRIGHTENED"
        self.frightened_timer = duration

    def die(self, duration: int):
        self.state = "DEAD"
        self.dead_timer = duration

    def respawn(self):
        self.x = self.home_x
        self.y = self.home_y
        self.rx = float(self.home_x)
        self.ry = float(self.home_y)
        self.state = "CHASE"
        self.frightened_timer = 0
        self.dead_timer = 0

    # dt = ch hal aybqa in9s htta tsali o9t li hrban fiha ghost
    def update(self, dt: float):
        speed = 5.0
        self.rx += (self.x - self.rx) * min(1.0, speed * dt)
        self.ry += (self.y - self.ry) * min(1.0, speed * dt)
        if self.state == "FRIGHTENED":
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.state = "CHASE"
                self.frightened_timer = 0
        elif self.state == "DEAD":
            self.dead_timer -= dt
            if self.dead_timer <= 0:
                self.respawn()

    def move(self, maze: Maze, player: Player, dt: float = 0):
        if self.frozen:
            return
        self.move_timer += dt
        if self.move_timer < 0.4:
            return
        self.move_timer = 0
        if self.state == "DEAD":
            return
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        no_reverse = [(dx, dy) for dx, dy in directions
                      if not (dx == -self.last_dx and dy == -self.last_dy)]
        valid = [(dx, dy) for dx, dy in no_reverse if maze.can_move(self.x, self.y, dx, dy)]
        if not valid:
            valid = [(dx, dy) for dx, dy in directions if maze.can_move(self.x, self.y, dx, dy)]
        if self.state == "FRIGHTENED":
            if valid:
                (dx, dy) = random.choice(valid)
                self.x += dx
                self.y += dy
                self.last_dx, self.last_dy = dx, dy
        elif self.state == "CHASE":
            if valid:
                (dx, dy) = min(valid, key=lambda d: (self.x+d[0]-player.x)**2 + (self.y+d[1]-player.y)**2)
                self.x += dx
                self.y += dy
                self.last_dx, self.last_dy = dx, dy
