"""Exercise real Qt widgets without requiring a visible desktop."""

import os
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar, cast
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QCloseEvent
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QMessageBox

    from mahjong.gui import MahjongWindow
except ImportError:
    raise unittest.SkipTest(
        "Install the desktop extra to run Qt tests."
    ) from None

from mahjong import MahjongGame
from mahjong.storage import save_game


class GuiTests(unittest.TestCase):
    app: ClassVar[QApplication]

    @classmethod
    def setUpClass(cls):
        cls.app = cast(
            QApplication, QApplication.instance() or QApplication([])
        )

    def setUp(self):
        self.window = MahjongWindow()
        self.window.show()
        self.app.processEvents()
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "game.json"

    def tearDown(self):
        self.window.dirty = False
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.temp.cleanup()

    def start(self):
        for field, name in zip(self.window.names, "ABCD"):
            field.setText(name)
        QTest.mouseClick(self.window.start_button, Qt.MouseButton.LeftButton)

    def enter_round(self, values=("12", "24", "8", "4"), winner=1):
        for field, value in zip(self.window.score_inputs, values):
            field.setText(value)
        if winner is not None:
            QTest.mouseClick(
                self.window.winners.button(winner), Qt.MouseButton.LeftButton
            )
        QTest.mouseClick(self.window.settle_button, Qt.MouseButton.LeftButton)

    def test_setup_validation_and_reference(self):
        QTest.mouseClick(self.window.start_button, Qt.MouseButton.LeftButton)
        self.assertIn("non-empty", self.window.setup_error.text())
        self.start()
        self.enter_round()
        self.assertEqual(
            cast(MahjongGame, self.window.game).totals,
            dict(A=-24, B=96, C=-28, D=-44),
        )
        self.assertEqual(cast(MahjongGame, self.window.game).east, "B")
        self.assertEqual(self.window.round_title.text(), "Round 2")
        self.assertEqual(
            [v.text() for v in self.window.total_values],
            ["-24", "+96", "-28", "-44"],
        )
        self.assertIn("B +96", self.window.result.text())
        self.assertEqual(len(self.window.history_rows), 1)
        self.assertIn("B +96", self.window.history_rows[0].text())
        self.assertIn("Hand values", self.window.detail.text())
        self.assertEqual(self.window.winners.checkedId(), -1)
        self.assertTrue(all(not f.text() for f in self.window.score_inputs))
        self.window.settle()
        self.assertEqual(cast(MahjongGame, self.window.game).round_number, 1)

    def test_bad_inputs_do_not_commit(self):
        self.start()
        self.enter_round(winner=None)
        self.assertIn("Select", self.window.round_error.text())
        for value, message in [
            ("abc", "whole-number"),
            ("3", "even"),
            ("-2", "non-negative"),
            ("20", "22"),
        ]:
            self.enter_round(("12", value, "8", "4"))
            self.assertIn(message, self.window.round_error.text())
            self.assertEqual(
                cast(MahjongGame, self.window.game).round_number, 0
            )
            self.assertEqual(self.window.score_inputs[1].text(), value)

    def test_east_streak_rotates_and_history_is_selectable(self):
        self.start()
        for _ in range(4):
            self.enter_round(("22", "0", "0", "0"), winner=0)
        self.assertEqual(cast(MahjongGame, self.window.game).east, "B")
        self.assertIn("0 of 4", self.window.streak_label.text())
        self.window.history_rows[0].click()
        self.assertIn("Round 1", self.window.detail.text())
        self.assertIn("East: A", self.window.detail.text())

    def test_save_and_reopen(self):
        self.start()
        self.enter_round()
        with patch(
            "mahjong.gui.QFileDialog.getSaveFileName",
            return_value=(str(self.path), ""),
        ):
            self.assertTrue(self.window.save())
        self.assertFalse(self.window.dirty)
        self.window.new_game()
        self.assertEqual(self.window.pages.currentIndex(), 0)
        with patch(
            "mahjong.gui.QFileDialog.getOpenFileName",
            return_value=(str(self.path), ""),
        ):
            self.window.open_game()
        self.assertEqual(cast(MahjongGame, self.window.game).east, "B")
        self.assertEqual(cast(MahjongGame, self.window.game).round_number, 1)
        self.assertEqual(self.window.pages.currentIndex(), 1)
        self.assertIn("Saved", self.window.file_status.text())

    def test_cancelled_and_failed_file_operations(self):
        self.assertFalse(self.window.save())
        self.start()
        with patch(
            "mahjong.gui.QFileDialog.getSaveFileName", return_value=("", "")
        ):
            self.assertFalse(self.window.save())
        with patch(
            "mahjong.gui.QFileDialog.getOpenFileName", return_value=("", "")
        ):
            self.window.open_game()
        game = self.window.game
        self.path.write_text("invalid")
        with (
            patch(
                "mahjong.gui.QFileDialog.getOpenFileName",
                return_value=(str(self.path), ""),
            ),
            patch("mahjong.gui.QMessageBox.warning") as warning,
        ):
            self.window.open_game()
            warning.assert_called_once()
        self.assertIs(self.window.game, game)
        with (
            patch(
                "mahjong.gui.QFileDialog.getSaveFileName",
                return_value=(str(self.path), ""),
            ),
            patch("mahjong.gui.save_game", side_effect=OSError("disk error")),
            patch("mahjong.gui.QMessageBox.warning"),
        ):
            self.assertFalse(self.window.save())
        self.assertTrue(self.window.dirty)

    def test_unsaved_game_can_cancel_save_or_discard(self):
        self.start()
        game = self.window.game
        with patch(
            "mahjong.gui.QMessageBox.question",
            return_value=QMessageBox.StandardButton.Cancel,
        ):
            self.window.new_game()
            self.assertIs(self.window.game, game)
            event = QCloseEvent()
            self.window.closeEvent(event)
            self.assertFalse(event.isAccepted())
        with (
            patch(
                "mahjong.gui.QMessageBox.question",
                return_value=QMessageBox.StandardButton.Save,
            ),
            patch.object(self.window, "save", return_value=False),
        ):
            self.assertFalse(self.window._can_leave())
        with patch(
            "mahjong.gui.QMessageBox.question",
            return_value=QMessageBox.StandardButton.Discard,
        ):
            self.window.new_game()
        self.assertIsNone(self.window.game)
        self.assertFalse(self.window.save_button.isEnabled())

    def test_open_can_be_cancelled_without_replacing_game(self):
        self.start()
        game = self.window.game
        save_game(MahjongGame(["W", "X", "Y", "Z"]), self.path)
        with (
            patch(
                "mahjong.gui.QFileDialog.getOpenFileName",
                return_value=(str(self.path), ""),
            ),
            patch(
                "mahjong.gui.QMessageBox.question",
                return_value=QMessageBox.StandardButton.Cancel,
            ),
        ):
            self.window.open_game()
        self.assertIs(self.window.game, game)

    def test_internal_error_is_visible_and_does_not_commit(self):
        self.start()
        with (
            patch.object(
                self.window.game,
                "play_round",
                side_effect=RuntimeError("not zero-sum"),
            ),
            patch("mahjong.gui.QMessageBox.critical") as error,
        ):
            self.enter_round()
        error.assert_called_once()
        self.assertEqual(cast(MahjongGame, self.window.game).round_number, 0)

    def test_player_names_are_plain_text(self):
        for field, name in zip(
            self.window.names, ["<b>A</b>", "李", "Zoë", "Ana"]
        ):
            field.setText(name)
        self.window.start_game()
        self.assertEqual(
            self.window.total_names[0].textFormat(), Qt.TextFormat.PlainText
        )
        self.assertEqual(self.window.total_names[0].text(), "<b>A</b>")
