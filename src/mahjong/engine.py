"""UI-independent settlement and game state, following SPEC.md."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
from itertools import combinations

from .winds import WINDS, Wind


def validate_hand_value(player: str, value: int) -> None:
    # bool is an int subclass, but is not a hand value.
    if type(value) is not int:
        raise ValueError(f"Hand value for {player} must be an integer.")
    if value < 0:
        raise ValueError(f"Hand value for {player} must be non-negative.")
    if value % 2:
        raise ValueError(f"Hand value for {player} must be even.")


def _check_zero_sum(values: Mapping[str, int], label: str) -> None:
    # Explicit checks remain active even when Python runs with -O.
    if sum(values.values()) != 0:
        raise RuntimeError(f"Calculation error: {label} is not zero-sum.")


class MahjongGame:
    """Four fixed seats; rounds commit only after validation and invariants pass.

    Public state properties return immutable values or independent snapshots.
    ``calculate_round`` previews a settlement; ``play_round`` commits it.
    """

    def __init__(self, players: Sequence[str]):
        if isinstance(players, (str, bytes)) or len(players) != 4:
            raise ValueError("Exactly four players are required.")
        if any(not isinstance(p, str) or not p.strip() for p in players):
            raise ValueError("Player names must be non-empty strings.")
        if len(set(players)) != 4:
            raise ValueError("Player names must be unique.")
        self._players = tuple(players)
        self._east_index = 0
        self._east_win_streak = 0
        self._completed_rounds = 0
        self._totals = dict.fromkeys(self._players, 0)
        self._history: list[dict] = []

    @property
    def players(self) -> tuple[str, ...]:
        return self._players

    @property
    def initial_east(self) -> str:
        return self.players[0]

    @property
    def seat_winds(self) -> dict[str, Wind]:
        return {
            player: WINDS[(index - self.east_index) % 4]
            for index, player in enumerate(self.players)
        }

    @property
    def round_wind(self) -> Wind:
        """North remains the displayed Round Wind once the game is over."""
        return WINDS[min(self._completed_rounds, 3)]

    @property
    def completed_rounds(self) -> int:
        return self._completed_rounds

    @property
    def game_over(self) -> bool:
        return self.completed_rounds == 4

    def _require_active(self) -> None:
        if self.game_over:
            raise ValueError("The North Round is complete. Start a new game.")

    @property
    def east_index(self) -> int:
        return self._east_index

    @property
    def east(self) -> str:
        return self.players[self.east_index]

    @property
    def east_win_streak(self) -> int:
        return self._east_win_streak

    @property
    def totals(self) -> dict[str, int]:
        return self._totals.copy()

    @property
    def history(self) -> list[dict]:
        return deepcopy(self._history)

    @property
    def round_number(self) -> int:
        """Legacy name: number of recorded hands, including unsuccessful hands."""
        return len(self._history)

    def calculate_round(
        self, scores: Mapping[str, int], winner: str
    ) -> dict[str, int]:
        """Return net changes without changing game state."""
        self._require_active()
        if not isinstance(scores, Mapping) or set(scores) != set(self.players):
            raise ValueError(
                "Scores must be provided for exactly the four players."
            )
        if winner not in self.players:
            raise ValueError("Winner must be one of the four players.")
        for player, value in scores.items():
            validate_hand_value(player, value)
        if scores[winner] < 22:
            raise ValueError("Winner must have at least 22 points.")

        changes = dict.fromkeys(self.players, 0)
        for first, second in combinations(self.players, 2):
            if winner in (first, second):
                receiver = winner
                payer = second if first == winner else first
                amount = scores[winner]
            else:
                difference = scores[first] - scores[second]
                if difference == 0:
                    continue
                receiver, payer = (
                    (first, second) if difference > 0 else (second, first)
                )
                amount = abs(difference)
            if self.east in (payer, receiver):
                amount *= 2
            changes[payer] -= amount
            changes[receiver] += amount

        _check_zero_sum(changes, "round")
        return changes

    def play_round(self, scores: Mapping[str, int], winner: str) -> dict:
        """Settle a round, update East, and return an independent history entry."""
        # Validate before copying so malformed input receives a clear error.
        changes = self.calculate_round(scores, winner)
        _check_zero_sum(changes, "round")
        totals = {p: self._totals[p] + changes[p] for p in self.players}
        _check_zero_sum(totals, "cumulative totals")

        streak = self.east_win_streak + 1 if winner == self.east else 0
        next_index = self.east_index
        if winner != self.east or streak == 4:
            next_index = (next_index + 1) % 4
            streak = 0

        round_completed = next_index != self.east_index and next_index == 0
        completed_rounds = self.completed_rounds + int(round_completed)
        entry = {
            "round": self.round_number + 1,
            "kind": "settled",
            "round_wind": self.round_wind,
            "seat_winds": self.seat_winds,
            "round_completed": round_completed,
            "next_round_wind": WINDS[min(completed_rounds, 3)],
            "game_over": completed_rounds == 4,
            "east": self.east,
            "winner": winner,
            "scores": dict(scores),
            "changes": changes.copy(),
            "totals": totals.copy(),
            "next_east": self.players[next_index],
            "east_win_streak": streak,
        }
        self._completed_rounds = completed_rounds
        self._totals = totals
        self._east_index = next_index
        self._east_win_streak = streak
        self._history.append(entry)
        return deepcopy(entry)

    def restart_hand(self) -> dict:
        """Record an unsuccessful hand; retain scores, Winds and East streak.

        The table declares that fewer than eight tiles remain; this scorekeeper
        does not simulate the wall or infer that condition from tile draws.
        """
        self._require_active()
        _check_zero_sum(self._totals, "cumulative totals")
        changes = dict.fromkeys(self.players, 0)
        _check_zero_sum(changes, "round")
        entry = {
            "round": self.round_number + 1,
            "kind": "restarted",
            "round_wind": self.round_wind,
            "seat_winds": self.seat_winds,
            "round_completed": False,
            "next_round_wind": self.round_wind,
            "game_over": False,
            "east": self.east,
            "winner": None,
            "scores": {},
            "changes": changes,
            "totals": self.totals,
            "next_east": self.east,
            "east_win_streak": self.east_win_streak,
        }
        self._history.append(entry)
        return deepcopy(entry)
