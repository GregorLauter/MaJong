"""Locate supplied artwork in a source checkout or an installed package."""

from pathlib import Path


def asset_path(name: str) -> Path:
    bundled = Path(__file__).parent / "assets" / name
    return (
        bundled
        if bundled.is_file()
        else Path(__file__).parents[2] / "assets" / name
    )
