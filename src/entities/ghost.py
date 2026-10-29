from src.maze import Maze
from src.entities.entity import Entity
from src.entities.player import Player


class Ghost(Entity):
    """A ghost enemy in the maze.

    A ghost has three states: CHASE (follows the player), FRIGHTENED
    (flees and can be eaten) and DEAD (waits, then respawns in its
    corner).
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize the ghost in its corner."""
        super().__init__(x, y)
        self.home_x = x
        self.home_y = y
        self.state = "CHASE"
        self.frightened_timer = 0.0
        self.dead_timer = 0.0
        self.frozen = False
        self.move_timer = 0.0
        self.last_dx = 0
        self.last_dy = 0
        self.rx = float(x)
        self.ry = float(y)

    def frighten(self, duration: int) -> None:
        """Make the ghost edible for a while."""
        self.state = "FRIGHTENED"
        self.frightened_timer = duration

    def die(self, duration: int) -> None:
        """Mark the ghost as eaten."""
        self.state = "DEAD"
        self.dead_timer = duration

    def respawn(self) -> None:
        """Put the ghost back in its corner in the CHASE state."""
        self.x = self.home_x
        self.y = self.home_y
        self.rx = float(self.home_x)
        self.ry = float(self.home_y)
        self.state = "CHASE"
        self.frightened_timer = 0
        self.dead_timer = 0

    def update(self, dt: float) -> None:
        """Update the timers and the smooth drawing position."""
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

    def ai_move(self, maze: Maze, player: Player, dt: float = 0) -> None:
        """Move the ghost one cell according to its state.

        The ghost steps every 0.4 seconds and avoids turning back. In CHASE
        it takes the direction that brings it closest to the player, in
        FRIGHTENED it picks a random one, and when DEAD or frozen it does
        not move.
        """
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
        valid = [(dx, dy) for dx, dy in no_reverse
                 if maze.can_move(self.x, self.y, dx, dy)]
        if not valid:
            valid = [(dx, dy) for dx, dy in directions
                     if maze.can_move(self.x, self.y, dx, dy)]
        if self.state == "FRIGHTENED":
            if valid:
                dx, dy = max(valid,
                             key=lambda d: (self.x+d[0]-player.x)**2
                             + (self.y+d[1]-player.y)**2)
                super().move(dx, dy, maze)
                self.last_dx, self.last_dy = dx, dy
        elif self.state == "CHASE":
            if valid:
                dx, dy = min(valid,
                             key=lambda d: (self.x+d[0]-player.x)**2
                             + (self.y+d[1]-player.y)**2)
                super().move(dx, dy, maze)
                self.last_dx, self.last_dy = dx, dy
