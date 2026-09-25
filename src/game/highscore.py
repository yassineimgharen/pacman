import json
import re


def load_score(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = json.loads(file.read())
        # ila makantch content list
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
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error: Failed to save scores to {path}. Error: {e}")


def add_score(scores: list, name: str, score: int) -> list:
    if score < 0:
        print("Warning: score cannot be negative, ignoring.")
        return scores
    name = name.strip()[:10]
    if not re.match(r"^[A-Za-z0-9 ]+$", name):
        print("Warning: invalid name, using 'Player'")
        name = "Player"
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:10]  # khlli 10 lwlin
