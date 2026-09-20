"""Offline Qt desktop interface. Scoring is delegated to the engine."""

import sys
from pathlib import Path
from typing import cast

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QFont,
    QIcon,
    QKeySequence,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .artwork import asset_path
from .engine import MahjongGame
from .rules import rules_text
from .storage import load_game, save_game

STYLE = """
QWidget { color: #203e35; font-size: 14px; }
QMainWindow, QWidget#canvas { background: #f5f3ec; }
QFrame#sidebar { background: #173e34; }
QFrame#sidebar QLabel { color: #f5f3ec; background: transparent; }
QLabel#brand { font-size: 31px; font-weight: 600; letter-spacing: 1px; }
QLabel#eyebrow { font-size: 11px; letter-spacing: 2px; color: #777b6d; }
QLabel#title { font-size: 34px; font-weight: 600; }
QLabel#subtitle { color: #737b70; font-size: 14px; }
QLabel#section { font-size: 20px; font-weight: 600; }
QLabel#metric { font-size: 25px; font-weight: 600; }
QLabel#badge { background: #e7eddf; color: #315a45; padding: 8px 12px;
              border-radius: 8px; font-size: 12px; }
QLabel#error { color: #a33e32; font-size: 13px; }
QLabel#result { background: #e7eddf; padding: 15px; border-radius: 10px; }
QFrame#card { background: #fffefa; border: 1px solid #e0e3d8;
              border-radius: 14px; }
QLineEdit { background: #fffefa; border: 1px solid #cfd7c9;
            border-radius: 8px; padding: 12px; selection-background-color: #376c55; }
QLineEdit:focus { border: 2px solid #527a5a; padding: 11px; }
QPushButton { border: 1px solid #cfd7c9; border-radius: 8px;
              padding: 11px 18px; background: #fffefa; font-weight: 500; }
QPushButton:hover { background: #e9eddf; }
QPushButton:pressed { background: #dce5d4; }
QPushButton#primary { background: #214f3d; color: #ffffff; border: none; }
QPushButton#primary:hover { background: #32684e; }
QPushButton#primary:disabled { background: #a5b5a7; }
QPushButton#winner:checked { background: #e4b866; border-color: #e4b866;
                           color: #263e32; }
QPushButton#side { background: transparent; color: #f5f3ec;
                  border: 1px solid #577468; text-align: left; }
QPushButton#side:hover { background: #315748; }
QPushButton#side:disabled { color: #718f80; border-color: #3a5d4e; }
QPushButton#history { text-align: left; padding: 14px; }
QPushButton#history:checked { background: #e3eadb; border-color: #9eb098; }
QScrollArea { border: none; background: transparent; }
"""


def label(text: str, style: str = "", wrap: bool = False) -> QLabel:
    item = QLabel(text)
    item.setTextFormat(Qt.TextFormat.PlainText)
    item.setObjectName(style)
    item.setWordWrap(wrap)
    return item


def button(text: str, callback, style: str = "") -> QPushButton:
    item = QPushButton(text)
    item.setObjectName(style)
    item.setCursor(Qt.CursorShape.PointingHandCursor)
    item.clicked.connect(callback)
    return item


class MahjongWindow(QMainWindow):
    """One window for setup, round entry, totals, and saved game history."""

    def __init__(self):
        super().__init__()
        self.game: MahjongGame | None = None
        self.save_path: Path | None = None
        self.dirty = False
        self.setWindowTitle("Mah Jong · The scorekeeper")
        self.resize(1120, 800)
        self.setMinimumSize(880, 680)
        self.setStyleSheet(STYLE)
        root = QWidget()
        root.setObjectName("canvas")
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(226)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(26, 34, 26, 28)
        side.setSpacing(15)
        self.banner = QLabel()
        self.banner.setAccessibleName("Mah Jong banner")
        self.banner.setPixmap(
            QPixmap(str(asset_path("mah_jong_banner.png"))).scaled(
                174,
                150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        side.addWidget(self.banner)
        side.addWidget(label("Mah Jong", "brand"))
        side.addWidget(label("THE SCOREKEEPER", "eyebrow"))
        side.addSpacing(35)
        side.addWidget(button("＋  New game", self.new_game, "side"))
        side.addWidget(button("Open game…", self.open_game, "side"))
        self.save_button = button("Save game…", self.save, "side")
        self.save_button.setEnabled(False)
        side.addWidget(self.save_button)
        self.rules_button = button("Rules / Regeln", self.show_rules, "side")
        side.addWidget(self.rules_button)
        side.addStretch()
        side.addWidget(label("Four seats.\nOne shared table.", wrap=True))
        side.addSpacing(10)
        side.addWidget(
            label("Chinese Classical\nOffline · On your laptop", wrap=True)
        )
        layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        layout.addWidget(self.pages, 1)
        self._build_setup()
        self._build_table()
        for title, shortcut, callback in (
            ("Save game", QKeySequence.StandardKey.Save, self.save),
            ("Open game", QKeySequence.StandardKey.Open, self.open_game),
            ("New game", QKeySequence.StandardKey.New, self.new_game),
        ):
            action = QAction(title, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(callback)
            self.addAction(action)

    def _page(self) -> QVBoxLayout:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        widget.setObjectName("canvas")
        scroll.setWidget(widget)
        self.pages.addWidget(scroll)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(38, 32, 38, 30)
        layout.setSpacing(16)
        return layout

    def _card(self, parent: QVBoxLayout) -> QVBoxLayout:
        card = QFrame()
        card.setObjectName("card")
        parent.addWidget(card)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)
        return layout

    def _build_setup(self):
        page = self._page()
        page.addWidget(label("WELCOME TO THE TABLE", "eyebrow"))
        page.addWidget(label("A good game.\nBeautifully kept.", "title"))
        page.addWidget(
            label(
                "Keep the focus on your tiles. We’ll take care of the scores.",
                "subtitle",
                True,
            )
        )
        page.addSpacing(16)
        card = self._card(page)
        card.addWidget(label("Who’s playing?", "section"))
        card.addWidget(
            label(
                "After determining initial Winds at the table, enter players "
                "in East/South/West/North order (counterclockwise).",
                "subtitle",
                True,
            )
        )
        self.names: list[QLineEdit] = []
        for number, wind in enumerate(("East", "South", "West", "North"), 1):
            row = QHBoxLayout()
            title = label(f"0{number}   {wind}")
            title.setFixedWidth(110)
            row.addWidget(title)
            entry = QLineEdit()
            entry.setMinimumHeight(44)
            entry.setPlaceholderText(f"{wind} player’s name")
            entry.setAccessibleName(f"{wind} player name")
            entry.returnPressed.connect(self.start_game)
            row.addWidget(entry)
            self.names.append(entry)
            card.addLayout(row)
        self.setup_error = label("", "error", True)
        card.addWidget(self.setup_error)
        self.start_button = button(
            "Start a game  →", self.start_game, "primary"
        )
        card.addWidget(self.start_button)
        page.addWidget(
            label(
                "East moves automatically. Save a game to pick it up another day.",
                "subtitle",
                True,
            )
        )
        page.addStretch()

    def _build_table(self):
        page = self._page()
        heading = QHBoxLayout()
        titles = QVBoxLayout()
        titles.addWidget(label("YOUR TABLE", "eyebrow"))
        self.round_title = label("Round 1", "title")
        titles.addWidget(self.round_title)
        heading.addLayout(titles)
        heading.addStretch()
        self.east_label = label("", "badge")
        heading.addWidget(self.east_label)
        page.addLayout(heading)
        self.streak_label = label("", "subtitle", True)
        page.addWidget(self.streak_label)

        cards = QHBoxLayout()
        self.total_names: list[QLabel] = []
        self.total_values: list[QLabel] = []
        for _ in range(4):
            frame = QFrame()
            frame.setObjectName("card")
            stack = QVBoxLayout(frame)
            stack.setContentsMargins(15, 15, 15, 15)
            name = label("", "subtitle", True)
            value = label("0", "metric")
            stack.addWidget(name)
            stack.addWidget(value)
            self.total_names.append(name)
            self.total_values.append(value)
            cards.addWidget(frame, 1)
        page.addLayout(cards)

        card = self._card(page)
        row = QHBoxLayout()
        row.addWidget(label("Settle this hand", "section"))
        row.addStretch()
        row.addWidget(label("Even values · Winner ≥ 22", "subtitle"))
        card.addLayout(row)
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(10)
        for col, text in enumerate(("PLAYER", "HAND VALUE", "WINNER")):
            grid.addWidget(label(text, "eyebrow"), 0, col)
        self.player_labels: list[QLabel] = []
        self.score_inputs: list[QLineEdit] = []
        self.winners = QButtonGroup(self)
        self.winners.setExclusive(True)
        for index in range(4):
            name = label("", wrap=True)
            self.player_labels.append(name)
            grid.addWidget(name, index + 1, 0)
            score = QLineEdit()
            score.setPlaceholderText("0")
            score.setMinimumWidth(90)
            score.setMinimumHeight(44)
            score.returnPressed.connect(self.settle)
            self.score_inputs.append(score)
            grid.addWidget(score, index + 1, 1)
            won = QPushButton("Won")
            won.setMinimumHeight(44)
            won.setObjectName("winner")
            won.setCheckable(True)
            won.setCursor(Qt.CursorShape.PointingHandCursor)
            self.winners.addButton(won, index)
            grid.addWidget(won, index + 1, 2)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        card.addLayout(grid)
        self.round_error = label("", "error", True)
        card.addWidget(self.round_error)
        self.settle_button = button("Settle hand  →", self.settle, "primary")
        card.addWidget(self.settle_button)
        self.restart_button = button(
            "Unsuccessful hand — restart", self.restart_hand
        )
        card.addWidget(self.restart_button)
        card.addWidget(
            label(
                "Fewer than 8 tiles remain: restart without changing scores or East.",
                "subtitle",
                True,
            )
        )
        self.result = label("", "result", True)
        self.result.hide()
        page.addWidget(self.result)

        page.addWidget(label("Hand history", "section"))
        # Real buttons avoid synthesized table accessibility nodes on macOS.
        self.history_rows: list[QPushButton] = []
        self.history_group = QButtonGroup(self)
        self.history_group.setExclusive(True)
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(8)
        page.addLayout(self.history_layout)
        self.detail = label(
            "Completed rounds will appear here.", "subtitle", True
        )
        page.addWidget(self.detail)
        self.file_status = label("Not saved yet", "subtitle", True)
        page.addWidget(self.file_status)
        page.addStretch()

    def start_game(self):
        try:
            game = MahjongGame([entry.text().strip() for entry in self.names])
        except ValueError as error:
            self.setup_error.setText(str(error))
            return
        self.game = game
        self.save_path = None
        self.dirty = True
        self.setup_error.clear()
        self._reset_inputs()
        self.result.hide()
        self.refresh()
        self.pages.setCurrentIndex(1)
        self.score_inputs[0].setFocus()

    def _reset_inputs(self):
        for score in self.score_inputs:
            score.clear()
        self.winners.setExclusive(False)
        for won in self.winners.buttons():
            won.setChecked(False)
        self.winners.setExclusive(True)
        self.round_error.clear()

    def settle(self):
        if self.game is None:
            return
        winner_index = self.winners.checkedId()
        if winner_index < 0:
            self.round_error.setText("Select the player who won this round.")
            return
        try:
            scores = {}
            for player, field in zip(self.game.players, self.score_inputs):
                try:
                    scores[player] = int(field.text().strip())
                except ValueError:
                    raise ValueError(
                        f"Enter a whole-number hand value for {player}."
                    ) from None
            result = self.game.play_round(
                scores, self.game.players[winner_index]
            )
        except ValueError as error:
            self.round_error.setText(str(error))
            return
        except RuntimeError as error:
            QMessageBox.critical(self, "Settlement failed", str(error))
            return
        self.dirty = True
        summary = "   ·   ".join(
            f"{p} {v:+d}" for p, v in result["changes"].items()
        )
        self.result.setText(f"Hand {result['round']} settled\n{summary}")
        self.result.show()
        self._reset_inputs()
        self.refresh()
        self.score_inputs[0].setFocus()

    def restart_hand(self):
        if self.game is None:
            return
        try:
            self.game.restart_hand()
        except (ValueError, RuntimeError) as error:
            self.round_error.setText(str(error))
            return
        self.dirty = True
        self._reset_inputs()
        self.result.setText(
            "Unsuccessful hand recorded. Scores and Winds unchanged."
        )
        self.result.show()
        self.refresh()

    def show_rules(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Rules / Regeln")
        dialog.resize(780, 700)
        layout = QVBoxLayout(dialog)
        language = QComboBox()
        language.addItems(["English", "Deutsch"])
        language.setAccessibleName("Rules language / Regelsprache")
        layout.addWidget(language)
        content = QTextBrowser()
        content.setOpenExternalLinks(False)
        layout.addWidget(content)

        def display_rules(index: int):
            try:
                content.setMarkdown(rules_text("en" if index == 0 else "de"))
            except (OSError, ValueError) as error:
                content.setPlainText(f"Could not load rules: {error}")

        language.currentIndexChanged.connect(display_rules)
        display_rules(0)
        dialog.exec()
        dialog.deleteLater()

    def refresh(self):
        if self.game is None:
            return
        game = self.game
        self.save_button.setEnabled(True)
        self.round_title.setText(
            "Game complete"
            if game.game_over
            else f"Hand {game.round_number + 1}"
        )
        self.settle_button.setEnabled(not game.game_over)
        self.restart_button.setEnabled(not game.game_over)
        for field in self.score_inputs:
            field.setEnabled(not game.game_over)
        for won in self.winners.buttons():
            won.setEnabled(not game.game_over)
        self.east_label.setText(f"EAST   {game.east}")
        self.streak_label.setText(
            f"{game.round_wind.value} Round  ·  "
            f"{game.east} is East  ·  {game.east_win_streak} of 4 consecutive wins"
            + (
                "  ·  North circuit complete — start a new game."
                if game.game_over
                else ""
            )
        )
        for i, player in enumerate(game.players):
            self.total_names[i].setText(player)
            self.total_values[i].setText(f"{game.totals[player]:+d}")
            self.player_labels[i].setText(
                f"{player}  ·  {game.seat_winds[player].value}"
            )
            self.score_inputs[i].setAccessibleName(f"Hand value for {player}")
            self.winners.button(i).setAccessibleName(f"{player} won")
        history = game.history
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            assert item is not None
            widget = item.widget()
            if widget is not None:
                self.history_group.removeButton(cast(QPushButton, widget))
                widget.deleteLater()
        self.history_rows = []
        for row, entry in enumerate(history):
            changes = "   ·   ".join(
                f"{p} {entry['changes'][p]:+d}" for p in game.players
            )
            outcome = (
                "Unsuccessful — restarted"
                if entry["kind"] == "restarted"
                else f"{entry['winner']} won"
            )
            text = (
                f"Hand {entry['round']}  ·  {entry['round_wind'].value} Round"
                f"  ·  {outcome}"
                f"  ·  Next East: {entry['next_east']}\n{changes}"
            )
            item_button = button(
                text,
                lambda checked=False, index=row: self.show_round_detail(index),
                "history",
            )
            item_button.setCheckable(True)
            self.history_group.addButton(item_button, row)
            self.history_rows.append(item_button)
            self.history_layout.addWidget(item_button)
        if history:
            self.history_rows[-1].setChecked(True)
            self.show_round_detail(len(history) - 1)
        else:
            self.detail.setText("Completed rounds will appear here.")
        self.file_status.setText(
            (f"{self.save_path.name}" if self.save_path else "Not saved yet")
            + ("  ·  Unsaved changes" if self.dirty else "  ·  Saved")
        )

    def show_round_detail(self, row: int):
        if self.game is None or not 0 <= row < self.game.round_number:
            return
        entry = self.game.history[row]
        hands = " · ".join(f"{p}: {v}" for p, v in entry["scores"].items())
        totals = " · ".join(f"{p}: {v:+d}" for p, v in entry["totals"].items())
        self.detail.setText(
            f"Hand {entry['round']} · {entry['round_wind'].value} Round · East: {entry['east']}\n"
            + (
                "Unsuccessful hand — restarted\n"
                if entry["winner"] is None
                else f"Winner: {entry['winner']}\n"
            )
            + f"Hand values — {hands}\nTotals after round — {totals}"
        )

    def save(self) -> bool:
        if self.game is None:
            return False
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Mah Jong game",
            str(self.save_path or "My game.majong.json"),
            "Mah Jong game (*.json)",
        )
        if not filename:
            return False
        try:
            save_game(self.game, Path(filename))
        except OSError as error:
            QMessageBox.warning(self, "Could not save game", str(error))
            return False
        self.save_path = Path(filename)
        self.dirty = False
        self.refresh()
        return True

    def _can_leave(self) -> bool:
        if not self.dirty:
            return True
        choice = QMessageBox.question(
            self,
            "Save this game?",
            "Save your completed rounds before leaving this game?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if choice == QMessageBox.StandardButton.Save:
            return self.save()
        return choice == QMessageBox.StandardButton.Discard

    def new_game(self):
        if not self._can_leave():
            return
        self.game = None
        self.save_path = None
        self.dirty = False
        self.save_button.setEnabled(False)
        for field in self.names:
            field.clear()
        self.setup_error.clear()
        self.pages.setCurrentIndex(0)
        self.names[0].setFocus()

    def open_game(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Mah Jong game", "", "Mah Jong game (*.json)"
        )
        if not filename:
            return
        try:
            game = load_game(Path(filename))
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Could not open game", str(error))
            return
        if not self._can_leave():
            return
        self.game = game
        self.save_path = Path(filename)
        self.dirty = False
        self._reset_inputs()
        self.result.hide()
        self.refresh()
        self.pages.setCurrentIndex(1)

    def closeEvent(self, event: QCloseEvent):
        if self._can_leave():
            event.accept()
        else:
            event.ignore()


def main() -> int:
    app = cast(QApplication, QApplication.instance() or QApplication(sys.argv))
    app.setWindowIcon(QIcon(str(asset_path("mah_jong_icon.png"))))
    app.setApplicationName("Mah Jong")
    app.setOrganizationName("Mah Jong")
    app.setFont(QFont("Arial", 13))
    window = MahjongWindow()
    window.show()
    if "--smoke-test" in sys.argv:
        QTimer.singleShot(100, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
