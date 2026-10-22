from src.maze import Maze


class Entity:
    """Base class for all moving entities in the maze."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize entity position and direction."""
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def move(self, dx: int, dy: int, maze: Maze) -> bool:
        """Move entity in direction (dx, dy) if no wall blocks it.

        Returns True if move was successful, False otherwise.
        """
        if maze.can_move(self.x, self.y, dx, dy):
            self.x += dx
            self.y += dy
            self.dx = dx
            self.dy = dy
            return True
        return False
