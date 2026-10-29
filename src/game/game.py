"""Game container that holds the player and the highscores."""

from src.entities.player import Player
from src.game.highscore import load_score
from src.game.level import Level


class Game():
    """Holds the state of one game and builds its levels."""
    def __init__(self, cfg: dict):
        """Create the player and load the highscores."""
        self.cfg = cfg
        self.player = Player(0, 0, cfg["lives"])
        self.scores = load_score(cfg["highscore_filename"])

    def start_level(self, level_index: int) -> Level:
        """Create the level at the given index.

        Returns:
            The new Level, with the player placed in the center.
        """
        lvl = self.cfg["levels"][level_index]
        return Level(lvl["width"],
                     lvl["height"],
                     lvl["seed"],
                     self.player,
                     self.cfg)
