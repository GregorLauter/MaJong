import random
import unittest
from unittest.mock import patch

from mahjong import MahjongGame
from mahjong.winds import Wind


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.game = MahjongGame(["A", "B", "C", "D"])
        self.scores = dict(A=12, B=24, C=8, D=4)

    def snapshot(self):
        g = self.game
        return g.east, g.east_win_streak, g.totals, g.history, g.round_number

    def test_reference_example(self):
        result = self.game.play_round(self.scores, "B")
        expected = dict(A=-24, B=96, C=-28, D=-44)
        self.assertEqual(result["changes"], expected)
        self.assertEqual(self.game.totals, expected)
        self.assertEqual(self.game.east, "B")
        self.assertEqual(self.game.east_win_streak, 0)

    def test_initial_state(self):
        self.assertEqual(
            self.snapshot(), ("A", 0, dict.fromkeys("ABCD", 0), [], 0)
        )
        self.assertEqual(self.game.players, tuple("ABCD"))

    def test_preview_does_not_change_state(self):
        before = self.snapshot()
        self.game.calculate_round(self.scores, "B")
        self.assertEqual(self.snapshot(), before)

    def test_east_winner_receives_double(self):
        result = self.game.play_round(dict(A=22, B=0, C=0, D=0), "A")
        self.assertEqual(result["changes"], dict(A=132, B=-44, C=-44, D=-44))
        self.assertEqual((self.game.east, self.game.east_win_streak), ("A", 1))

    def test_equal_zero_losers_and_east_pays_double(self):
        changes = self.game.calculate_round(dict(A=0, B=22, C=0, D=0), "B")
        self.assertEqual(changes, dict(A=-44, B=88, C=-22, D=-22))

    def test_equal_nonzero_losers(self):
        changes = self.game.calculate_round(dict(A=8, B=24, C=8, D=8), "B")
        self.assertEqual(changes, dict(A=-48, B=96, C=-24, D=-24))

    def test_losing_east_receives_double(self):
        changes = self.game.calculate_round(dict(A=12, B=24, C=8, D=8), "B")
        self.assertEqual(changes, dict(A=-32, B=96, C=-32, D=-32))

    def test_losing_east_pays_double_to_other_losers(self):
        changes = self.game.calculate_round(dict(A=4, B=24, C=8, D=8), "B")
        self.assertEqual(changes, dict(A=-64, B=96, C=-16, D=-16))

    def test_winner_receives_absolute_value_even_if_loser_has_more(self):
        changes = self.game.calculate_round(dict(A=30, B=22, C=30, D=30), "B")
        self.assertEqual(changes, dict(A=-44, B=88, C=-22, D=-22))

    def test_rotate_to_next_seat_not_winner(self):
        self.game.play_round(dict(A=0, B=0, C=22, D=0), "C")
        self.assertEqual(self.game.east, "B")

    def test_four_consecutive_east_wins(self):
        for count in range(1, 5):
            self.game.play_round(dict(A=22, B=0, C=0, D=0), "A")
            self.assertEqual(self.game.east, "A" if count < 4 else "B")
            self.assertEqual(
                self.game.east_win_streak, count if count < 4 else 0
            )
        self.game.play_round(dict(A=0, B=22, C=0, D=0), "B")
        self.assertEqual(self.game.east_win_streak, 1)

    def test_streak_reset_and_rotation_wrap(self):
        scores = dict.fromkeys("ABCD", 22)
        self.game.play_round(scores, "A")
        self.game.play_round(scores, "A")
        for winner, next_east in [
            ("C", "B"),
            ("A", "C"),
            ("A", "D"),
            ("B", "A"),
        ]:
            self.game.play_round(scores, winner)
            self.assertEqual(
                (self.game.east, self.game.east_win_streak), (next_east, 0)
            )
        self.game.play_round(scores, "A")
        self.assertEqual((self.game.east, self.game.east_win_streak), ("A", 1))

    def test_player_validation(self):
        for players in [
            [],
            ["A"] * 3,
            list("ABCDE"),
            list("ABCA"),
            ["", "B", "C", "D"],
            ["  ", "B", "C", "D"],
            [1, "B", "C", "D"],
            "ABCD",
        ]:
            with self.subTest(players=players), self.assertRaises(ValueError):
                MahjongGame(players)  # type: ignore[arg-type]  # Invalid input test.

    def test_invalid_scores_leave_state_unchanged(self):
        for value, message in [
            (-2, "non-negative"),
            (1, "even"),
            (21, "even"),
            (25, "even"),
            (2.0, "integer"),
            ("2", "integer"),
            (True, "integer"),
            (None, "integer"),
        ]:
            with self.subTest(value=value):
                scores = dict(self.scores, A=value)
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, message):
                    self.game.play_round(scores, "B")  # type: ignore[arg-type]
                self.assertEqual(self.snapshot(), before)

    def test_missing_extra_and_malformed_scores(self):
        for scores in [
            dict(A=12, B=24, C=8),
            dict(self.scores, E=0),
            dict(A=12, B=24, C=8, E=4),
            None,
            [12, 24, 8, 4],
        ]:
            with (
                self.subTest(scores=scores),
                self.assertRaisesRegex(ValueError, "exactly"),
            ):
                self.game.play_round(scores, "B")  # type: ignore[arg-type]
        self.assertEqual(self.game.round_number, 0)

    def test_unknown_winner(self):
        with self.assertRaisesRegex(ValueError, "Winner"):
            self.game.play_round(self.scores, "E")

    def test_winner_minimum(self):
        for value in (0, 4, 20):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "at least 22"),
            ):
                self.game.play_round(dict(self.scores, B=value), "B")
        self.game.play_round(dict(self.scores, B=22), "B")
        self.assertEqual(self.game.round_number, 1)

    def test_history_records_and_cumulative_totals(self):
        first = self.game.play_round(self.scores, "B")
        second = self.game.play_round(self.scores, "B")
        self.assertEqual(
            first,
            dict(
                round=1,
                kind="settled",
                round_wind=Wind.EAST,
                seat_winds=dict(zip("ABCD", Wind)),
                round_completed=False,
                next_round_wind=Wind.EAST,
                game_over=False,
                east="A",
                winner="B",
                scores=self.scores,
                changes=dict(A=-24, B=96, C=-28, D=-44),
                totals=dict(A=-24, B=96, C=-28, D=-44),
                next_east="B",
                east_win_streak=0,
            ),
        )
        self.assertEqual(second["changes"], dict(A=-36, B=144, C=-48, D=-60))
        self.assertEqual(second["totals"], dict(A=-60, B=240, C=-76, D=-104))
        self.assertEqual(second["east"], "B")
        self.assertEqual(second["round"], 2)
        self.assertEqual(self.game.history, [first, second])

    def test_input_and_output_snapshots_cannot_mutate_state(self):
        players = list("ABCD")
        game = MahjongGame(players)
        players[0] = "X"
        entry = game.play_round(self.scores, "B")
        self.scores["A"] = 100
        entry["scores"]["A"] = 200
        entry["totals"]["A"] = 200
        game.totals["A"] = 200
        history = game.history
        history[0]["changes"]["A"] = 200
        history.clear()
        self.assertEqual(game.players, tuple("ABCD"))
        self.assertEqual(game.history[0]["scores"]["A"], 12)
        self.assertEqual(game.history[0]["changes"]["A"], -24)
        self.assertEqual(game.totals["A"], -24)

    def test_round_invariant_failure_does_not_commit(self):
        before = self.snapshot()
        with patch.object(
            self.game, "calculate_round", return_value=dict(A=1, B=0, C=0, D=0)
        ):
            with self.assertRaisesRegex(RuntimeError, "round"):
                self.game.play_round(self.scores, "B")
        self.assertEqual(self.snapshot(), before)

    def test_cumulative_invariant_failure_does_not_commit(self):
        self.game._totals["A"] = 1  # Simulate an internal state corruption.
        before = self.snapshot()
        with self.assertRaisesRegex(RuntimeError, "cumulative"):
            self.game.play_round(self.scores, "B")
        self.assertEqual(self.snapshot(), before)

    def test_many_rounds_against_independent_formula(self):
        rng = random.Random(42)
        expected_totals = dict.fromkeys("ABCD", 0)
        for _ in range(1000):
            if self.game.game_over:
                self.game = MahjongGame(list("ABCD"))
                expected_totals = dict.fromkeys("ABCD", 0)
            scores = {p: 2 * rng.randrange(100) for p in "ABCD"}
            winner = rng.choice(self.game.players)
            scores[winner] = max(22, scores[winner])
            east = self.game.east
            expected = {}
            for p in self.game.players:
                if p == winner:
                    expected[p] = scores[p] * (6 if p == east else 4)
                else:
                    expected[p] = -scores[winner] * (
                        2 if east in (p, winner) else 1
                    )
                    expected[p] += sum(
                        (scores[p] - scores[q]) * (2 if east in (p, q) else 1)
                        for q in self.game.players
                        if q not in (p, winner)
                    )
            result = self.game.play_round(scores, winner)
            self.assertEqual(result["changes"], expected)
            for p in self.game.players:
                expected_totals[p] += expected[p]
            self.assertEqual(self.game.totals, expected_totals)
            self.assertEqual(sum(result["changes"].values()), 0)
            self.assertEqual(sum(self.game.totals.values()), 0)


if __name__ == "__main__":
    unittest.main()
