"""Portable game files. Restore by replaying validated rounds through the engine."""

import json
import os
import tempfile
from pathlib import Path

from .engine import MahjongGame


def save_game(game: MahjongGame, path: Path) -> None:
    """Atomically save completed rounds; never write partial round inputs."""
    payload = {
        "format": "majong-game",
        "version": 2,
        "players": list(game.players),
        "rounds": [
            {"scores": r["scores"], "winner": r["winner"]}
            for r in game.history
        ],
    }
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def load_game(path: Path) -> MahjongGame:
    """Load a complete, validated game or raise without changing live state."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError("This is not a valid MahJong game file.") from error
    if (
        not isinstance(payload, dict)
        or payload.get("format") != "majong-game"
        or type(payload.get("version")) is not int
        or payload["version"] not in (1, 2)
    ):
        raise ValueError("Unsupported MahJong game file format or version.")
    players = payload.get("players")
    rounds = payload.get("rounds")
    if not isinstance(players, list) or not isinstance(rounds, list):
        raise ValueError("The game file must contain players and rounds.")
    game = MahjongGame(players)
    for number, entry in enumerate(rounds, 1):
        if not isinstance(entry, dict) or set(entry) != {"scores", "winner"}:
            raise ValueError(f"Invalid data for round {number}.")
        try:
            if payload["version"] == 2 and entry["winner"] is None:
                if entry["scores"] != {}:
                    raise ValueError("An unsuccessful hand has no scores.")
                game.restart_hand()
            else:
                game.play_round(entry["scores"], entry["winner"])
        except ValueError as error:
            raise ValueError(f"Invalid round {number}: {error}") from error
    return game
