from src.entities.player import Player
from src.game.highscore import load_score
from src.game.level import Level


class Game():
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.player = Player(0, 0, cfg["lives"])
        self.scores = load_score(cfg["highscore_filename"])

    def start_level(self, level_index: int) -> Level:
        lvl = self.cfg["levels"][level_index]
        return Level(lvl["width"],
                     lvl["height"],
                     lvl["seed"],
                     self.player,
                     self.cfg)
