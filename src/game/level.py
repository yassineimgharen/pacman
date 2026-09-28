from src.entities.player import Player
from src.entities.ghost import Ghost
from src.maze import Maze


class Level:
    def __init__(self,
                 width: int,
                 height: int,
                 seed: int,
                 player: Player,
                 cnfg: dict):
        self.width = width
        self.height = height
        self.seed = seed
        self.player = player
        self.cnfg = cnfg
        self.maze = Maze(self.width, self.height, self.seed)

        # place player at center:
        cx, cy = self.maze.get_center()
        self.player.respawn(cx, cy)

        # get corners of the maze
        corners = self.maze.get_corners()

        # build pacgums set — all walkable cells except corners and center:
        self.pacgums = set()
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in corners and (x, y) != (cx, cy):
                    self.pacgums.add((x, y))

        self.super_pacgums = set(corners)

        self.ghosts = [Ghost(x, y) for x, y in corners]

        self.timer = cnfg["level_max_time"]

    # called every frame, moves ghosts, checks collisions, updates timer
    def update(self, dt: float):
        self.timer -= dt

        for ghost in self.ghosts:
            ghost.move(self.maze, self.player)

        for ghost in self.ghosts:
            if ghost.x == self.player.x and ghost.y == self.player.y:
                if ghost.state == "CHASE" and not self.player.invincible:
                    self.player.lose_life()
                    self.player.respawn(*self.maze.get_center())
                elif ghost.state == "FRIGHTENED":
                    ghost.die(self.cnfg["ghost_respawn_delay"])
                    self.player.add_score(self.cnfg["points_per_ghost"])

        pos = (self.player.x, self.player.y)
        if pos in self.pacgums:
            self.pacgums.remove(pos)
            self.player.add_score(self.cnfg["points_per_pacgum"])
        elif pos in self.super_pacgums:
            self.super_pacgums.remove(pos)
            self.player.add_score(self.cnfg["points_per_super_pacgum"])
            for ghost in self.ghosts:
                ghost.frighten(self.cnfg["frightened_duration"])

        for ghost in self.ghosts:
            ghost.update(dt)

    def is_won(self) -> bool:
        return len(self.pacgums) == 0

    def is_lost(self) -> bool:
        return self.player.lives <= 0 or self.timer <= 0
