"""Winds in fixed counterclockwise seating and Round order."""

from enum import Enum


class Wind(str, Enum):
    EAST = "East"
    SOUTH = "South"
    WEST = "West"
    NORTH = "North"

    @property
    def number(self) -> int:
        """Matching Flower/Season number (1–4)."""
        return WINDS.index(self) + 1


WINDS = tuple(Wind)
