"""Load, save and update the top 10 highscores."""

import json
import re


def load_score(path: str) -> list:
    """Load the highscore list from a JSON file.

    Returns:
        The list of {"name", "score"} entries, or an empty list if the
        file is missing, empty or invalid.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            raw = file.read()
        # empty file
        if not raw.strip():
            return []
        content = json.loads(raw)
        if not isinstance(content, list):
            print(f"Warning: invalid format in {path}, resetting scores.")
            return []
        return content
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {path}")
        return []


def save_scores(path: str, scores: list) -> None:
    """Save the highscore list to a JSON file.

    Errors are printed and do not stop the game.
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error: Failed to save scores to {path}. Error: {e}")


def add_score(scores: list, name: str, score: int) -> list:
    """Add a score and keep only the 10 best.

    The name is cut to 10 characters and replaced by "Player" if it
    contains anything other than letters, digits and spaces. A negative
    score is ignored.

    Returns:
        The new list, sorted from best to worst, with at most 10 entries.
    """
    if score < 0:
        print("Warning: score cannot be negative, ignoring.")
        return scores
    name = name.strip()[:10]
    if not re.match(r"^[A-Za-z0-9 ]+$", name):
        print("Warning: invalid name, using 'Player'")
        name = "Player"
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:10]
