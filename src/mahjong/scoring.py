"""Explicit hand components → base points → doubles, exclusively per RULES.md.

A Chow's tile is its lowest tile. Loose tiles score zero. This API accepts an
already arranged hand; it does not search for arrangements or adjudicate claims.
The caller supplies the current seat and Round Winds before settlement.
"""

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from .winds import Wind


class Suit(str, Enum):
    CHARACTERS = "Characters"
    BAMBOO = "Bamboo"
    CIRCLES = "Circles"
    WIND = "Wind"
    DRAGON = "Dragon"


class Dragon(str, Enum):
    RED = "Red"
    GREEN = "Green"
    WHITE = "White"


class MeldKind(str, Enum):
    CHOW = "Chow"
    PUNG = "Pung"
    KONG = "Kong"


class Exposure(str, Enum):
    EXPOSED = "Exposed"
    CONCEALED = "Concealed"
    EXTENDED = "Extended"


class BonusKind(str, Enum):
    FLOWER = "Flower"
    SEASON = "Season"


@dataclass(frozen=True)
class Tile:
    suit: Suit
    value: Union[int, Wind, Dragon]

    def __post_init__(self) -> None:
        if not isinstance(self.suit, Suit):
            raise ValueError("Use a Suit enum for a tile's suit.")
        if self.suit == Suit.WIND:
            valid = isinstance(self.value, Wind)
        elif self.suit == Suit.DRAGON:
            valid = isinstance(self.value, Dragon)
        else:
            valid = type(self.value) is int and 1 <= self.value <= 9
        if not valid:
            raise ValueError("Tile value does not match its suit.")

    @property
    def is_major(self) -> bool:
        return self.suit in (Suit.WIND, Suit.DRAGON) or self.value in (1, 9)


@dataclass(frozen=True)
class Meld:
    kind: MeldKind
    tile: Tile
    exposure: Exposure = Exposure.EXPOSED

    def __post_init__(self) -> None:
        if (
            not isinstance(self.kind, MeldKind)
            or not isinstance(self.tile, Tile)
            or not isinstance(self.exposure, Exposure)
        ):
            raise ValueError("A meld needs a kind, tile and exposure.")
        if self.exposure == Exposure.EXTENDED and self.kind != MeldKind.KONG:
            raise ValueError("Only a Kong may be extended.")
        if self.kind == MeldKind.CHOW and (
            type(self.tile.value) is not int or self.tile.value > 7
        ):
            raise ValueError("A Chow must start with a suited tile from 1–7.")


@dataclass(frozen=True)
class BonusTile:
    kind: BonusKind
    number: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.kind, BonusKind)
            or type(self.number) is not int
            or not 1 <= self.number <= 4
        ):
            raise ValueError("A Flower or Season needs a number from 1–4.")


@dataclass(frozen=True)
class Hand:
    melds: tuple[Meld, ...] = ()
    pair: Optional[Tile] = None
    bonuses: tuple[BonusTile, ...] = ()
    loose_tiles: tuple[Tile, ...] = ()

    def __post_init__(self) -> None:
        for name, expected in (
            ("melds", Meld),
            ("bonuses", BonusTile),
            ("loose_tiles", Tile),
        ):
            items = getattr(self, name)
            if not isinstance(items, (tuple, list)) or any(
                not isinstance(item, expected) for item in items
            ):
                raise ValueError(f"Invalid {name} components.")
            object.__setattr__(self, name, tuple(items))
        if self.pair is not None and not isinstance(self.pair, Tile):
            raise ValueError("Supply at most one scoring pair as a Tile.")
        if len(self.melds) > 4:
            raise ValueError("A hand may contain at most four melds.")
        if len(set(self.bonuses)) != len(self.bonuses):
            raise ValueError("Each Flower/Season exists only once.")
        tiles = list(self.loose_tiles)
        if self.pair is not None:
            tiles.extend([self.pair] * 2)
        for meld in self.melds:
            if meld.kind == MeldKind.CHOW:
                assert isinstance(meld.tile.value, int)
                tiles.extend(
                    Tile(meld.tile.suit, meld.tile.value + offset)
                    for offset in range(3)
                )
            else:
                tiles.extend(
                    [meld.tile] * (4 if meld.kind == MeldKind.KONG else 3)
                )
        if any(count > 4 for count in Counter(tiles).values()):
            raise ValueError(
                "There are only four copies of each ordinary tile."
            )


@dataclass(frozen=True)
class HandScore:
    ordinary_base: int
    mahjong_points: int
    zero_base_bonus: int
    doubles: int

    @property
    def base_points(self) -> int:
        return self.ordinary_base + self.mahjong_points + self.zero_base_bonus

    @property
    def final_value(self) -> int:
        return self.base_points * 2**self.doubles


def score_hand(
    hand: Hand, *, seat_wind: Wind, round_wind: Wind, winner: bool = False
) -> HandScore:
    """Score declared components; no East payment multiplier is applied here.

    Winners require four melds and a pair, with no loose material. Losing hands
    may be incomplete; supply one selected scoring pair and leave the rest loose.
    """
    if (
        not isinstance(hand, Hand)
        or not isinstance(seat_wind, Wind)
        or not isinstance(round_wind, Wind)
        or type(winner) is not bool
    ):
        raise ValueError("Supply a Hand, two Wind enums and a boolean winner.")
    if winner and (
        len(hand.melds) != 4 or hand.pair is None or hand.loose_tiles
    ):
        raise ValueError("Mah Jong requires four melds plus one pair.")
    base = 0
    doubles = 0
    for meld in hand.melds:
        if meld.kind == MeldKind.CHOW:
            continue
        points = 8 if meld.kind == MeldKind.KONG else 2
        points *= 2 if meld.tile.is_major else 1
        points *= 2 if meld.exposure != Exposure.EXPOSED else 1
        base += points
        doubles += int(meld.kind == MeldKind.KONG)
        if meld.tile.suit == Suit.WIND:
            doubles += 1 + int(meld.tile.value == seat_wind)
            doubles += int(meld.tile.value == round_wind)
        elif meld.tile.suit == Suit.DRAGON:
            doubles += 1
    if hand.pair is not None and (
        hand.pair.suit == Suit.DRAGON
        or (hand.pair.suit == Suit.WIND and hand.pair.value == seat_wind)
    ):
        base += 2
    base += 4 * len(hand.bonuses)
    doubles += sum(tile.number == seat_wind.number for tile in hand.bonuses)
    return HandScore(
        ordinary_base=base,
        mahjong_points=20 if winner else 0,
        zero_base_bonus=2 if winner and base == 0 else 0,
        doubles=doubles,
    )
