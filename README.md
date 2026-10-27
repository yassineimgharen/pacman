*This project has been created as part of the 42 curriculum by <login>.*

# Pac-Man

## Description

A Python remake of the arcade classic Pac-Man, built with **pygame** and an
object-oriented, modular architecture.

Each level is a maze produced by an external **A-Maze-ing** package (written
by another group and used as-is). Pac-Man must eat every pacgum in the maze
while four ghosts chase him. Super-pacgums in the four corners make the
ghosts edible for a few seconds. The game has 10+ levels, a time limit per
level, a persistent top-10 highscore table and a cheat mode for evaluation.

Game loop: **Main menu → play levels → win or lose → enter name → main menu**.

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

`make install` installs pygame, the assigned maze generator
(`mazegenerator-00001-py3-none-any.whl`), flake8 and mypy.

### Running

```bash
make run
# or
python3 pac-man.py config.json
```

The program takes exactly one argument: a JSON configuration file.

### Other Makefile rules

| Rule | Action |
|---|---|
| `make debug` | Run the game under `pdb` |
| `make lint` | Run `flake8 .` and `mypy` with the required flags |
| `make lint-strict` | Run `flake8 .` and `mypy --strict` |
| `make clean` | Remove `__pycache__`, `.mypy_cache`, `.pytest_cache`, `build`, `dist` |

### Packaging

The game is packaged with [PyInstaller](https://pyinstaller.org/) using the
`pacman.spec` file at the root of the repository. Build it from the activated
virtual environment, so that pygame and the maze generator are bundled:

```bash
source venv/bin/activate
python -m PyInstaller --clean pacman.spec
```

This produces a single executable, `dist/pacman`. Run it from a folder that
contains a configuration file:

```bash
./dist/pacman config.json
```

PyInstaller does not cross-compile: a build made on Linux only runs on Linux.
Build on Windows to get `pacman.exe`.

### Controls

| Key | Action |
|---|---|
| Arrow keys / WASD | Move |
| SPACE | Pause / resume |
| ENTER | Start game (main menu), confirm name |
| Q | Quit (main menu) / end current game |

### Cheat mode

Cheat keys are always active during a game:

| Key | Cheat |
|---|---|
| I | Toggle invincibility |
| F | Toggle ghost freeze |
| L | Add one life |
| N | Skip the current level |

## Configuration

The configuration file is standard JSON. In addition, **every line whose
first non-space character is `#` is treated as a comment** and ignored.

```json
{
    # file where the top 10 is saved
    "highscore_filename": "highscores.json",
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "frightened_duration": 8,
    "ghost_respawn_delay": 5,
    "level_max_time": 90,
    "levels": [
        {"width": 15, "height": 15, "seed": 42},
        {"width": 15, "height": 15}
    ]
}
```

| Key | Type | Default | Rule |
|---|---|---|---|
| `highscore_filename` | string | `"highscores.json"` | non-empty |
| `lives` | int | `3` | ≥ 1 |
| `points_per_pacgum` | int | `10` | ≥ 0 |
| `points_per_super_pacgum` | int | `50` | ≥ 0 |
| `points_per_ghost` | int | `200` | ≥ 0 |
| `frightened_duration` | int (s) | `8` | ≥ 1 |
| `ghost_respawn_delay` | int (s) | `5` | ≥ 1 |
| `level_max_time` | int (s) | `90` | ≥ 0 |
| `levels` | list of objects | 10 default levels | see below |

Each entry of `levels`:

| Key | Type | Default | Rule |
|---|---|---|---|
| `width` | int | `21` | ≥ 5 |
| `height` | int | `21` | ≥ 5 |
| `seed` | int | `0` | ≥ 0; `0` means a random maze |

The first level should use a fixed seed (e.g. `42`); the other levels leave
`seed` out so that they are random.

### Faulty configuration handling

- **Missing or invalid value:** a warning is printed and the default is used.
- **Unknown keys:** ignored.
- **Fewer than 10 levels:** the list is padded with random 21×21 levels.
- **Missing file, invalid JSON or permission denied:** a clear error message
  is printed and the program exits with status 1 (no traceback).

When the level timer reaches 0, the game is over.

## Highscore

Highscores are stored in a JSON file in the project directory (name set by
`highscore_filename`). The file holds a list of entries sorted from best to
worst:

```json
[{"name": "milan", "score": 3440}, {"name": "Player", "score": 3300}]
```

How it works:

- **Loaded** when a game starts and **saved** after the player enters a name,
  and again when the application closes.
- **Top 10 only:** a new score is inserted, the list is sorted by score and
  cut to 10 entries.
- **Names:** at most 10 characters, letters, digits and spaces only. The
  name prompt only accepts those characters; an empty or invalid name
  becomes `Player`.
- **Scores:** non-negative integers; negative scores are rejected.
- **Robustness:** a missing, empty or invalid file gives an empty table
  instead of a crash. Write errors are printed and the game keeps running.
- The table is displayed on the main menu.

**Why this design:** a JSON file is human-readable, easy to inspect and reset
during an evaluation, needs only the standard library, and fits naturally
with the JSON configuration file.

## Maze Generation

Mazes come from the assigned **A-Maze-ing** package (`mazegenerator`),
installed from the wheel at the root of the repository and used without
modification. The `Maze` class (`src/maze.py`) is the adapter between that
package and the game:

```python
MazeGenerator(size=(width, height), perfect=False, seed=seed).maze
```

- `perfect=False` makes the generator open extra walls, creating loops, as
  Pac-Man needs corridors with several ways around.
- `seed=0` gives a random maze; any other value gives a reproducible maze.
- The result is a 2D grid `grid[y][x]` where each cell is a 4-bit wall mask:
  `1` = north, `2` = east, `4` = south, `8` = west. A cell equal to `15` is
  fully closed (part of the "42" pattern the generator draws in mazes of at
  least 14×10) and gets no pacgum.
- `Maze.can_move(x, y, dx, dy)` checks the wall bit of the current cell for
  the requested direction. The generator always sets a wall on both sides,
  so checking one cell is enough.
- If the generator raises an exception, the error is printed and the
  program exits cleanly.

## Implementation

- **Language / library:** Python 3.10+, pygame 2.6.
- **Main loop** (`pac-man.py`): 60 FPS loop that reads keyboard events,
  updates the level with the frame time `dt`, then draws the maze and HUD.
- **Level setup:** player in the centre of the maze, ghosts and
  super-pacgums in the four corners, pacgums on every other open cell.
- **Player:** moves one cell per key press, only where there is no wall.
  Score and lives are kept between levels.
- **Ghosts:** state machine with three states:
  - `CHASE`: at each step, picks the open direction that brings it closest
    to the player (without turning back), every 0.4 s.
  - `FRIGHTENED`: after a super-pacgum, moves randomly; can be eaten.
  - `DEAD`: after being eaten; returns to its corner after
    `ghost_respawn_delay` seconds.
- **Collisions:** a chasing ghost on the player's cell costs a life; the
  player and the ghosts go back to their starting positions.
- **Win / lose:** a level is won when every pacgum and super-pacgum is eaten;
  the game is lost when lives reach 0 or the timer runs out.
- **Quality:** the code passes `flake8` and `mypy` with the required flags
  (`make lint`).

## General Software Architecture

```
pac-man.py              entry point: argument check, main loop
src/
├── config.py           load + validate the JSON config (comments, defaults)
├── maze.py             Maze: adapter around the A-Maze-ing package
├── entities/
│   ├── entity.py       Entity: position, direction, wall-checked move
│   ├── player.py       Player(Entity): lives, score, invincibility
│   └── ghost.py        Ghost(Entity): CHASE / FRIGHTENED / DEAD + AI
├── game/
│   ├── game.py         Game: holds config, player, highscores; builds levels
│   ├── level.py        Level: maze, pacgums, ghosts, timer, update rules
│   └── highscore.py    load / save / add highscores
└── ui/
    ├── menu.py         main menu, name entry screen
    ├── hud.py          score, lives, level, time, controls panel
    └── renderer.py     draws background, walls, pacgums, player, ghosts
```

Relationships:

- `pac-man.py` uses `config.load()` to build the config, then a `Game`.
- `Game` owns one `Player` (shared by every level) and the highscore list,
  and creates a `Level` for each level index.
- `Level` owns a `Maze`, four `Ghost`s and the pacgum sets, and updates them
  every frame.
- `Player` and `Ghost` both inherit from `Entity`, which uses
  `Maze.can_move()` to respect walls.
- The `ui` modules only read the game state and draw it; they never change
  the rules.

## Project Management

<!-- TODO: link the project management directory once it exists -->
Planning, progress tracking, risk analysis and the acceptance test plan are
in the [project management directory](project_management/).

## Resources

- [pygame documentation](https://www.pygame.org/docs/)
- [Python `json` module](https://docs.python.org/3/library/json.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [PEP 8](https://peps.python.org/pep-0008/) and
  [PEP 257](https://peps.python.org/pep-0257/)
- [The Pac-Man Dossier](https://www.gamedeveloper.com/design/the-pac-man-dossier)
  (Jamey Pittman), how the original ghost AI works
- [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

### Use of AI

AI assistants (Claude, Amazon Q) were used to:

- explain parts of the subject and of the assigned maze package (wall-bit
  encoding);
- review the project against the subject and list missing features and bugs;
- fix type annotations so the code passes `mypy`, and adjust the Makefile and
  flake8 configuration;

All AI-generated content was reviewed, tested and is understood by the
author.
