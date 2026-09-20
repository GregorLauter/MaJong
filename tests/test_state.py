import unittest

from mahjong import MahjongGame
from mahjong.winds import Wind


class StateTests(unittest.TestCase):
    def setUp(self):
        self.game = MahjongGame(list("ABCD"))
        self.scores = dict.fromkeys("ABCD", 22)

    def rotate(self):
        game = self.game
        return game.play_round(
            self.scores, game.players[(game.east_index + 1) % 4]
        )

    def test_seat_winds_follow_fixed_physical_order(self):
        for expected in [
            (Wind.EAST, Wind.SOUTH, Wind.WEST, Wind.NORTH),
            (Wind.NORTH, Wind.EAST, Wind.SOUTH, Wind.WEST),
            (Wind.WEST, Wind.NORTH, Wind.EAST, Wind.SOUTH),
            (Wind.SOUTH, Wind.WEST, Wind.NORTH, Wind.EAST),
        ]:
            self.assertEqual(tuple(self.game.seat_winds.values()), expected)
            self.assertEqual(self.game.initial_east, "A")
            self.assertEqual(self.game.players, tuple("ABCD"))
            self.game.seat_winds.clear()
            self.assertEqual(len(self.game.seat_winds), 4)
            self.rotate()
        self.assertEqual(self.game.round_wind, Wind.SOUTH)

    def test_four_circuits_end_game_atomically(self):
        for completed, wind in enumerate(Wind):
            self.assertEqual(self.game.round_wind, wind)
            self.assertEqual(self.game.completed_rounds, completed)
            for rotation in range(4):
                entry = self.rotate()
                self.assertEqual(entry["round_wind"], wind)
                self.assertEqual(entry["round_completed"], rotation == 3)
                self.assertEqual(
                    entry["game_over"], completed == 3 and rotation == 3
                )
                self.assertEqual(sum(entry["changes"].values()), 0)
                self.assertEqual(sum(self.game.totals.values()), 0)
            self.assertEqual(self.game.east, "A")
        self.assertEqual(
            (self.game.completed_rounds, self.game.round_wind), (4, Wind.NORTH)
        )
        before = self.game.history
        for action in (
            lambda: self.game.play_round(self.scores, "A"),
            lambda: self.game.calculate_round(self.scores, "A"),
            self.game.restart_hand,
        ):
            with self.assertRaisesRegex(ValueError, "North Round"):
                action()
        self.assertEqual(self.game.history, before)

    def test_east_wins_and_restarts_do_not_prematurely_end_circuit(self):
        self.game.play_round(self.scores, "A")
        self.game.play_round(self.scores, "A")
        before = (
            self.game.totals,
            self.game.seat_winds,
            self.game.round_wind,
            self.game.east_win_streak,
        )
        entry = self.game.restart_hand()
        self.assertEqual(entry["kind"], "restarted")
        self.assertEqual(entry["changes"], dict.fromkeys("ABCD", 0))
        self.assertIsNone(entry["winner"])
        self.assertEqual(entry["scores"], {})
        self.assertEqual(
            (
                self.game.totals,
                self.game.seat_winds,
                self.game.round_wind,
                self.game.east_win_streak,
            ),
            before,
        )
        entry["totals"]["A"] = 999
        self.assertNotEqual(self.game.history[-1]["totals"]["A"], 999)
        self.game.play_round(self.scores, "A")
        self.assertEqual(self.game.east, "A")
        self.game.play_round(self.scores, "A")
        self.assertEqual((self.game.east, self.game.east_win_streak), ("B", 0))
        self.assertEqual(self.game.completed_rounds, 0)

    def test_fourth_east_win_can_complete_north_circuit(self):
        for _ in range(15):
            self.rotate()
        for count in range(4):
            entry = self.game.play_round(self.scores, "D")
            self.assertEqual(self.game.game_over, count == 3)
        self.assertTrue(entry["round_completed"])
        self.assertEqual((self.game.east, self.game.east_win_streak), ("A", 0))

    def test_failed_restart_does_not_commit(self):
        self.game._totals["A"] = 1
        with self.assertRaisesRegex(RuntimeError, "cumulative"):
            self.game.restart_hand()
        self.assertEqual(self.game.history, [])
