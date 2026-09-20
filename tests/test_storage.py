import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mahjong import MahjongGame
from mahjong.storage import load_game, save_game


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "game.json"
        self.game = MahjongGame(["A", "B", "C", "D"])

    def test_roundtrip_preserves_all_state_and_can_continue(self):
        for winner in ["B", "B", "B", "B", "B", "A", "B", "C"]:
            self.game.play_round(dict.fromkeys("ABCD", 24), winner)
        save_game(self.game, self.path)
        restored = load_game(self.path)
        self.assertEqual(restored.players, self.game.players)
        self.assertEqual(restored.history, self.game.history)
        self.assertEqual(restored.totals, self.game.totals)
        self.assertEqual(restored.east, self.game.east)
        self.assertEqual(restored.east_win_streak, self.game.east_win_streak)
        self.assertEqual(
            restored.play_round(dict.fromkeys("ABCD", 24), "D"),
            self.game.play_round(dict.fromkeys("ABCD", 24), "D"),
        )

    def test_empty_and_unicode_games(self):
        game = MahjongGame(["Zoë", "李", "Ömer", "Ana"])
        save_game(game, self.path)
        self.assertEqual(load_game(self.path).players, game.players)
        self.assertEqual(load_game(self.path).round_number, 0)

    def test_invalid_json_and_encoding(self):
        for data in (b"{", b"\xff"):
            self.path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "valid MaJong"):
                load_game(self.path)

    def test_invalid_schema(self):
        base = dict(
            format="majong-game", version=1, players=list("ABCD"), rounds=[]
        )
        for payload in [
            [],
            {},
            dict(base, version=2),
            dict(base, version=True),
            dict(base, players="ABCD"),
            dict(base, rounds={}),
            dict(base, players=list("ABCA")),
            dict(base, rounds=[None]),
            dict(base, rounds=[{"winner": "A"}]),
            dict(
                base,
                rounds=[{"winner": "A", "scores": dict.fromkeys("ABCD", 1)}],
            ),
        ]:
            with self.subTest(payload=payload):
                self.path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError):
                    load_game(self.path)

    def test_failed_save_preserves_existing_file_and_cleans_temp(self):
        save_game(self.game, self.path)
        original = self.path.read_bytes()
        with patch(
            "mahjong.storage.os.replace", side_effect=OSError("disk error")
        ):
            with self.assertRaises(OSError):
                save_game(self.game, self.path)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_missing_file(self):
        with self.assertRaises(OSError):
            load_game(self.path)
