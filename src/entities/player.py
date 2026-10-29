"""The Pac-Man player."""

from src.maze import Maze
from src.entities.entity import Entity


class Player(Entity):
    """The Pac-Man player controlled with the keyboard."""

    def __init__(self, x: int, y: int, lives: int) -> None:
        """Initialize the player."""
        super().__init__(x, y)
        self.lives = lives
        self.score = 0
        self.invincible = False
        self.death_flash = 0.0

    def move(self, dx: int, dy: int, maze: Maze) -> bool:
        """Move the player by (dx, dy) if no wall blocks it.

        Returns:
            True if the player moved, False otherwise.
        """
        return super().move(dx, dy, maze)

    def lose_life(self) -> None:
        """Remove one life from the player."""
        self.lives -= 1

    def respawn(self, x: int, y: int) -> None:
        """Put the player at (x, y) with no direction."""
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def add_score(self, points: int) -> None:
        """Add points to the score."""
        self.score += points
