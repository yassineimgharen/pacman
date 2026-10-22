from src.maze import Maze
from src.entities.entity import Entity


class Player(Entity):
    """Represents the Pac-Man player."""

    def __init__(self, x: int, y: int, lives: int) -> None:
        """Initialize player with position and lives."""
        super().__init__(x, y)
        self.lives = lives
        self.score = 0
        self.invincible = False
        self.death_flash = 0.0

    def move(self, dx: int, dy: int, maze: Maze) -> None:
        """Move player if no wall blocks the path."""
        super().move(dx, dy, maze)

    def lose_life(self) -> None:
        """Decrease player lives by 1."""
        self.lives -= 1

    def respawn(self, x: int, y: int) -> None:
        """Reset player position and direction."""
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def add_score(self, points: int) -> None:
        """Add points to player score."""
        self.score += points
