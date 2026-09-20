"""RULES.md tables and explicit stacking examples (no external variants)."""

import unittest

from mahjong.scoring import (
    BonusKind,
    BonusTile,
    Dragon,
    Exposure,
    Hand,
    Meld,
    MeldKind,
    Suit,
    Tile,
    score_hand,
)
from mahjong.winds import Wind


class ScoringTests(unittest.TestCase):
    def score(self, hand, seat=Wind.EAST, round_wind=Wind.SOUTH, winner=False):
        return score_hand(
            hand, seat_wind=seat, round_wind=round_wind, winner=winner
        )

    def chow_hand(self, **kwargs):
        return Hand(
            melds=tuple(
                Meld(MeldKind.CHOW, Tile(Suit.BAMBOO, n)) for n in (1, 2, 4, 7)
            ),
            pair=kwargs.pop("pair", Tile(Suit.CIRCLES, 5)),
            **kwargs,
        )

    def test_pung_and_kong_base_tables(self):
        categories = [
            *(
                Tile(suit, n)
                for suit in (Suit.BAMBOO, Suit.CIRCLES, Suit.CHARACTERS)
                for n in range(1, 10)
            ),
            *(Tile(Suit.WIND, wind) for wind in Wind),
            *(Tile(Suit.DRAGON, dragon) for dragon in Dragon),
        ]
        for tile in categories:
            major = tile.suit in (Suit.WIND, Suit.DRAGON) or tile.value in (
                1,
                9,
            )
            for kind, exposure, ordinary, high in [
                (MeldKind.PUNG, Exposure.EXPOSED, 2, 4),
                (MeldKind.PUNG, Exposure.CONCEALED, 4, 8),
                (MeldKind.KONG, Exposure.EXPOSED, 8, 16),
                (MeldKind.KONG, Exposure.CONCEALED, 16, 32),
                (MeldKind.KONG, Exposure.EXTENDED, 16, 32),
            ]:
                with self.subTest(tile=tile, kind=kind, exposure=exposure):
                    result = self.score(
                        Hand(melds=(Meld(kind, tile, exposure),))
                    )
                    self.assertEqual(
                        result.ordinary_base, high if major else ordinary
                    )
                    expected_doubles = int(kind == MeldKind.KONG)
                    if tile.suit == Suit.WIND:
                        expected_doubles += 1 + int(
                            tile.value in (Wind.EAST, Wind.SOUTH)
                        )
                    elif tile.suit == Suit.DRAGON:
                        expected_doubles += 1
                    self.assertEqual(result.doubles, expected_doubles)
                    self.assertEqual(
                        result.final_value,
                        result.base_points * 2**expected_doubles,
                    )
                    self.assertEqual(
                        (result.mahjong_points, result.zero_base_bonus), (0, 0)
                    )

    def test_chows_zero_exposed_and_concealed(self):
        for exposure in (Exposure.EXPOSED, Exposure.CONCEALED):
            result = self.score(
                Hand(
                    melds=(
                        Meld(MeldKind.CHOW, Tile(Suit.BAMBOO, 7), exposure),
                    )
                )
            )
            self.assertEqual(
                (result.base_points, result.doubles, result.final_value),
                (0, 0, 0),
            )

    def test_pairs_score_base_only(self):
        for tile, expected in [
            (Tile(Suit.BAMBOO, 1), 0),
            (Tile(Suit.BAMBOO, 5), 0),
            (Tile(Suit.WIND, Wind.EAST), 2),
            (
                Tile(Suit.WIND, Wind.SOUTH),
                0,
            ),  # Round Wind alone is not a scoring pair.
            (Tile(Suit.WIND, Wind.WEST), 0),
            *((Tile(Suit.DRAGON, dragon), 2) for dragon in Dragon),
        ]:
            with self.subTest(tile=tile):
                result = self.score(Hand(pair=tile))
                self.assertEqual(
                    (result.base_points, result.doubles), (expected, 0)
                )
        self.assertEqual(
            self.score(
                Hand(pair=Tile(Suit.WIND, Wind.EAST)), round_wind=Wind.EAST
            ).doubles,
            0,
        )

    def test_flowers_seasons_all_seat_numbers(self):
        for seat in Wind:
            for kind in BonusKind:
                for number in range(1, 5):
                    result = self.score(
                        Hand(bonuses=(BonusTile(kind, number),)), seat=seat
                    )
                    self.assertEqual(result.base_points, 4)
                    self.assertEqual(
                        result.doubles, int(number == seat.number)
                    )
            both = self.score(
                Hand(
                    bonuses=tuple(BonusTile(k, seat.number) for k in BonusKind)
                ),
                seat=seat,
            )
            self.assertEqual(
                (both.base_points, both.doubles, both.final_value), (8, 2, 32)
            )
        all_bonus = self.score(
            Hand(
                bonuses=tuple(
                    BonusTile(k, n) for k in BonusKind for n in range(1, 5)
                )
            )
        )
        self.assertEqual(
            (all_bonus.base_points, all_bonus.doubles, all_bonus.final_value),
            (32, 2, 128),
        )

    def test_wind_doubles_including_same_seat_and_round(self):
        for kind, base, kong in [
            (MeldKind.PUNG, 4, 0),
            (MeldKind.KONG, 16, 1),
        ]:
            hand = Hand(melds=(Meld(kind, Tile(Suit.WIND, Wind.SOUTH)),))
            for seat, round_wind, doubles in [
                (Wind.EAST, Wind.WEST, 1),  # generic Wind
                (Wind.SOUTH, Wind.WEST, 2),  # own Wind
                (Wind.EAST, Wind.SOUTH, 2),  # Round Wind
                (Wind.SOUTH, Wind.SOUTH, 3),  # both
            ]:
                result = self.score(hand, seat, round_wind)
                self.assertEqual(result.base_points, base)
                self.assertEqual(result.doubles, doubles + kong)
                self.assertEqual(
                    result.final_value, base * 2 ** (doubles + kong)
                )

    def test_stacking_multiplies_entire_base(self):
        hand = Hand(
            melds=(
                Meld(
                    MeldKind.KONG,
                    Tile(Suit.WIND, Wind.SOUTH),
                    Exposure.EXTENDED,
                ),
                Meld(MeldKind.PUNG, Tile(Suit.DRAGON, Dragon.RED)),
                Meld(MeldKind.PUNG, Tile(Suit.BAMBOO, 5), Exposure.CONCEALED),
                Meld(MeldKind.CHOW, Tile(Suit.CIRCLES, 1)),
            ),
            pair=Tile(Suit.DRAGON, Dragon.WHITE),
            bonuses=(
                BonusTile(BonusKind.FLOWER, 2),
                BonusTile(BonusKind.SEASON, 2),
            ),
        )
        result = self.score(hand, Wind.SOUTH, Wind.SOUTH, winner=True)
        self.assertEqual(result.ordinary_base, 50)  # 32+4+4+0+2+4+4
        self.assertEqual(
            (result.mahjong_points, result.zero_base_bonus), (20, 0)
        )
        self.assertEqual((result.doubles, result.final_value), (7, 8960))
        loser = self.score(hand, Wind.SOUTH, Wind.SOUTH)
        self.assertEqual(loser.final_value, 6400)

    def test_minimum_winner_and_no_spurious_bonuses(self):
        result = self.score(self.chow_hand(), winner=True)
        self.assertEqual(
            (
                result.ordinary_base,
                result.mahjong_points,
                result.zero_base_bonus,
            ),
            (0, 20, 2),
        )
        self.assertEqual((result.doubles, result.final_value), (0, 22))
        self.assertEqual(self.score(self.chow_hand()).final_value, 0)
        for hand, base, final in [
            (self.chow_hand(pair=Tile(Suit.DRAGON, Dragon.GREEN)), 2, 22),
            (self.chow_hand(pair=Tile(Suit.WIND, Wind.EAST)), 2, 22),
            (self.chow_hand(bonuses=(BonusTile(BonusKind.FLOWER, 2),)), 4, 24),
            (self.chow_hand(bonuses=(BonusTile(BonusKind.FLOWER, 1),)), 4, 48),
        ]:
            result = self.score(hand, winner=True)
            self.assertEqual(
                (
                    result.ordinary_base,
                    result.zero_base_bonus,
                    result.final_value,
                ),
                (base, 0, final),
            )
        pungs = Hand(
            melds=tuple(
                Meld(MeldKind.PUNG, Tile(Suit.BAMBOO, n), Exposure.CONCEALED)
                for n in (2, 3, 4, 5)
            ),
            pair=Tile(Suit.BAMBOO, 6),
        )
        result = self.score(pungs, winner=True)
        self.assertEqual((result.doubles, result.final_value), (0, 36))

    def test_incomplete_and_loose_material_is_zero(self):
        result = self.score(
            Hand(
                loose_tiles=(
                    Tile(Suit.BAMBOO, 1),
                    Tile(Suit.BAMBOO, 2),
                    Tile(Suit.WIND, Wind.EAST),
                    Tile(Suit.DRAGON, Dragon.RED),
                )
            )
        )
        self.assertEqual(
            (result.base_points, result.doubles, result.final_value), (0, 0, 0)
        )
        self.assertEqual(self.score(Hand()).final_value, 0)

    def test_invalid_components_and_winning_structure(self):
        tile = Tile(Suit.BAMBOO, 3)
        invalid = [
            lambda: Tile("Bamboo", 1),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Tile(Suit.BAMBOO, True),
            lambda: Tile(Suit.BAMBOO, 10),
            lambda: Tile(Suit.WIND, 1),
            lambda: Tile(Suit.DRAGON, Wind.EAST),
            lambda: Meld("Pung", tile),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Meld(MeldKind.PUNG, None),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Meld(MeldKind.PUNG, tile, "Exposed"),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Meld(MeldKind.PUNG, tile, Exposure.EXTENDED),
            lambda: Meld(MeldKind.CHOW, Tile(Suit.WIND, Wind.EAST)),
            lambda: Meld(MeldKind.CHOW, Tile(Suit.BAMBOO, 8)),
            lambda: BonusTile(BonusKind.FLOWER, 0),
            lambda: BonusTile(BonusKind.FLOWER, 5),
            lambda: BonusTile(BonusKind.FLOWER, True),
            lambda: BonusTile("Flower", 1),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Hand(melds=(None,)),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Hand(melds=None),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Hand(pair=(tile, tile)),  # type: ignore[arg-type]  # Deliberately invalid.
            lambda: Hand(melds=(Meld(MeldKind.PUNG, tile),) * 5),
            lambda: Hand(bonuses=(BonusTile(BonusKind.FLOWER, 1),) * 2),
            lambda: Hand(melds=(Meld(MeldKind.PUNG, tile),), pair=tile),
            lambda: self.score(Hand(), winner=True),
            lambda: self.score(
                Hand(melds=self.chow_hand().melds), winner=True
            ),
            lambda: self.score(
                self.chow_hand(loose_tiles=(tile,)), winner=True
            ),
            lambda: self.score(Hand(), seat="East"),
            lambda: self.score(Hand(), round_wind="East"),
            lambda: self.score(Hand(), winner=1),
            lambda: self.score(None),
        ]
        for make in invalid:
            with self.subTest(make=make), self.assertRaises(ValueError):
                make()

    def test_component_inputs_are_immutable_snapshots(self):
        melds = [Meld(MeldKind.PUNG, Tile(Suit.BAMBOO, 3))]
        hand = Hand(melds=melds)  # type: ignore[arg-type]
        melds.clear()
        self.assertEqual(self.score(hand).final_value, 2)
