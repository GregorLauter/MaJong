import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from mahjong.cli import main


class CliTests(unittest.TestCase):
    def run_cli(self, inputs):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=inputs),
            redirect_stdout(output),
        ):
            main()
        return output.getvalue()

    def test_reference_and_second_round(self):
        output = self.run_cli(
            [
                "A",
                "B",
                "C",
                "D",
                "12",
                "24",
                "8",
                "4",
                "2",
                "",
                "12",
                "24",
                "8",
                "4",
                "2",
                "n",
            ]
        )
        for text in [
            "A: -24",
            "B: +96",
            "C: -28",
            "D: -44",
            "Next East: B",
            "ROUND 2",
            "Current East: B",
            "A: -60",
            "B: +240",
            "C: -76",
            "D: -104",
            "FINAL TOTALS",
        ]:
            self.assertIn(text, output)

    def test_invalid_inputs_are_reprompted(self):
        output = self.run_cli(
            [
                "",
                "A",
                "A",
                "B",
                "C",
                "D",
                "abc",
                "-2",
                "3",
                "12",
                "24",
                "8",
                "4",
                "abc",
                "0",
                "5",
                "2",
                "n",
            ]
        )
        for text in [
            "non-empty",
            "unique",
            "whole number",
            "non-negative",
            "even",
            "number from 1 to 4",
            "B: +96",
        ]:
            self.assertIn(text, output)

    def test_invalid_winner_value_retries_without_advancing(self):
        output = self.run_cli(
            [
                "A",
                "B",
                "C",
                "D",
                "12",
                "20",
                "8",
                "4",
                "2",
                "12",
                "24",
                "8",
                "4",
                "2",
                "n",
            ]
        )
        self.assertIn("at least 22", output)
        self.assertEqual(output.count("ROUND 1"), 2)
        self.assertNotIn("ROUND 2", output)
        self.assertIn("B: +96", output)

    def test_eof_and_interrupt_are_clean(self):
        for exception in (EOFError, KeyboardInterrupt):
            with self.subTest(exception=exception):
                output = self.run_cli([exception])
                self.assertIn("Game ended.", output)
                output = self.run_cli(["A", "B", "C", "D", "12", exception])
                self.assertIn("FINAL TOTALS", output)
                self.assertIn("A: +0", output)
                self.assertNotIn("ROUND CHANGES", output)

    def test_entry_points_in_real_processes(self):
        root = Path(__file__).resolve().parents[1]
        for args in (["majong.py"], ["-m", "mahjong"]):
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, *args],
                    cwd=root,
                    input="A\nB\nC\nD\n12\n24\n8\n4\n2\nn\n",
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                for text in [
                    "A: -24",
                    "B: +96",
                    "C: -28",
                    "D: -44",
                    "Next East: B",
                ]:
                    self.assertIn(text, result.stdout)

    def test_restart_and_game_completion(self):
        output = self.run_cli(
            ["A", "B", "C", "D", "0", "0", "0", "0", "r", "n"]
        )
        self.assertIn("Unsuccessful hand restarted", output)
        self.assertIn("Current East: A", output)
        self.assertIn("Round Wind: East", output)
        inputs = list("ABCD")
        for hand in range(16):
            inputs.extend(["22"] * 4 + [str((hand + 1) % 4 + 1)])
            if hand < 15:
                inputs.append("")
        output = self.run_cli(inputs)
        self.assertIn("Round Wind: North", output)
        self.assertIn("North Round complete. Game over.", output)
        self.assertNotIn("ROUND 17", output)


if __name__ == "__main__":
    unittest.main()
