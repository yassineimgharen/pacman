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

    def frighten(self, duration: int):
        self.state = "FRIGHTENED"
        self.frightened_timer = duration

    def die(self, duration: int):
        self.state = "DEAD"
        self.dead_timer = duration

    def respawn(self):
        self.x = self.home_x
        self.y = self.home_y
        self.state = "CHASE"
        self.frightened_timer = 0
        self.dead_timer = 0

    # dt = ch hal aybqa in9s htta tsali o9t li hrban fiha ghost
    def update(self, dt: int):
        if self.state == "FRIGHTENED":
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.state = "CHASE"
                self.frightened_timer = 0
        elif self.state == "DEAD":
            self.dead_timer -= dt
            if self.dead_timer <= 0:
                self.respawn()

    def move(self, maze: Maze, player: Player):
        if self.frozen:
            return
        if self.state == "DEAD":
            return
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        valid = [(dx, dy) for dx, dy in directions if maze.can_move(self.x, self.y, dx, dy)]
        if self.state == "FRIGHTENED":
            # return  possible valid moves
            if valid:
                (dx, dy) = random.choice(valid)
                self.x += dx
                self.y += dy
        elif self.state == "CHASE":
            # Move towards the player
            if valid:
                (dx, dy) = min(valid, key=lambda d: (self.x+d[0]-player.x)**2 + (self.y+d[1]-player.y)**2)
                self.x += dx
                self.y += dy
