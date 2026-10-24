import json
import sys


def _strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


def load(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        cleaned = _strip_comments(content)
        data = json.loads(cleaned)
        cfg = {}

        def _get(key, default):
            if key not in data:
                print(f"Warning: missing '{key}', using default {default}")
            return data.get(key, default)

        # validate and set default values for configuration parameters
        lives = _get("lives", 3)
        if not isinstance(lives, int) or lives < 1:
            print("Warning: invalid 'lives', using default 3")
            lives = 3
        cfg["lives"] = lives

        points_per_pacgum = _get("points_per_pacgum", 10)
        if not isinstance(points_per_pacgum, int) or points_per_pacgum < 0:
            print("Warning: invalid 'points_per_pacgum', using default 10")
            points_per_pacgum = 10
        cfg["points_per_pacgum"] = points_per_pacgum

        p_per_super_pacgum = _get("points_per_super_pacgum", 50)
        if not isinstance(p_per_super_pacgum, int) or p_per_super_pacgum < 0:
            print("Warning: invalid points_per_super_pacgum, using default 50")
            p_per_super_pacgum = 50
        cfg["points_per_super_pacgum"] = p_per_super_pacgum

        points_per_ghost = _get("points_per_ghost", 200)
        if not isinstance(points_per_ghost, int) or points_per_ghost < 0:
            print("Warning: invalid 'points_per_ghost', using default 200")
            points_per_ghost = 200
        cfg["points_per_ghost"] = points_per_ghost

        level_max_time = _get("level_max_time", 90)
        if not isinstance(level_max_time, int) or level_max_time < 0:
            print("Warning: invalid 'level_max_time', using default 90")
            level_max_time = 90
        cfg["level_max_time"] = level_max_time

        highscore_filename = _get("highscore_filename", "highscores.json")
        if not isinstance(highscore_filename, str) or not highscore_filename:
            print("Warning: invalid 'highscore_filename', using default highscores.json")
            highscore_filename = "highscores.json"
        cfg["highscore_filename"] = highscore_filename

        frightened_duration = _get("frightened_duration", 8)
        if not isinstance(frightened_duration, int) or frightened_duration < 1:
            print("Warning: invalid 'frightened_duration', using default 8")
            frightened_duration = 8
        cfg["frightened_duration"] = frightened_duration

        ghost_respawn_delay = _get("ghost_respawn_delay", 5)
        if not isinstance(ghost_respawn_delay, int) or ghost_respawn_delay < 1:
            print("Warning: invalid 'ghost_respawn_delay', using default 5")
            ghost_respawn_delay = 5
        cfg["ghost_respawn_delay"] = ghost_respawn_delay

        # validate levels
        levels = data.get("levels", [])
        if not isinstance(levels, list) or not all(isinstance(level, dict) for level in levels):
            print("Warning: invalid 'levels', using default []")
            levels = []

        validated_levels = []
        for i, level in enumerate(levels):
            width = level.get("width", 21)
            if not isinstance(width, int) or width < 5:
                print(f"Warning: invalid 'width' in level {i}, using default 21")
                width = 21
            height = level.get("height", 21)
            if not isinstance(height, int) or height < 5:
                print(f"Warning: invalid 'height' in level {i}, using default 21")
                height = 21
            seed = level.get("seed", 0)
            if not isinstance(seed, int) or seed < 0:
                print(f"Warning: invalid 'seed' in level {i}, using default 0")
                seed = 0
            validated_levels.append({"width": width, "height": height, "seed": seed})

        while len(validated_levels) < 10:
            validated_levels.append({"width": 21, "height": 21, "seed": 0})
        cfg["levels"] = validated_levels

        return cfg

    except FileNotFoundError:
        print("Configuration file not found.")
        sys.exit(1)
    # file kayn broken json
    except json.JSONDecodeError:
        print("Invalid JSON in config file")
        sys.exit(1)
    except PermissionError:
        print("Permission denied when accessing config file")
        sys.exit(1)
