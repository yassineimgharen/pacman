from src.maze import Maze


class Player:
    def __init__(self, x: int, y: int, lives: int):
        self.x = x
        self.y = y
        self.lives = lives
        self.score = 0
        self.dx = 0
        self.dy = 0

    def move(self, dx: int, dy: int, maze: Maze) -> None:
        if maze.can_move(self.x, self.y, dx, dy):
            self.x += dx
            self.y += dy
            self.dx = dx
            self.dy = dy

    def lose_life(self) -> None:
        self.lives -= 1

    def respawn(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def add_score(self, points: int) -> None:
        self.score += points
