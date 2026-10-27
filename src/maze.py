from mazegenerator import MazeGenerator
import sys


class Maze:
    def __init__(self, width: int, height: int, seed: int) -> None:
        try:
            mg = MazeGenerator(size=(width, height), perfect=False, seed=seed)
            self.grid: list[list[int]] = mg.maze
        except Exception as e:
            print(f"Maze generation failed: {e}")
            sys.exit(1)
        self.width = width
        self.height = height

    def can_move(self, x: int, y: int, dx: int, dy: int) -> bool:
        """
        Check if a move is possible from (x, y) in the direction (dx, dy).
        """
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.width and 0 <= ny < self.height):
            return False
        if dx == 1:
            bit = 2
        elif dx == -1:
            bit = 8
        elif dy == -1:
            bit = 1
        else:
            bit = 4
        return (self.grid[y][x] & bit) == 0

    def get_center(self) -> tuple[int, int]:
        """
        Get the center of the maze.
        """
        return (self.width // 2, self.height // 2)

    def get_corners(self) -> list[tuple[int, int]]:
        """
        Get the corners of the maze.
        """
        return [(0, 0),
                (self.width - 1, 0),
                (0, self.height - 1),
                (self.width - 1, self.height - 1)]
