"""Read the canonical bilingual rulebook, from source or a packaged copy."""

from pathlib import Path


def rules_text(language: str = "en") -> str:
    if language not in ("en", "de"):
        raise ValueError("Rules language must be 'en' or 'de'.")
    bundled = Path(__file__).with_name("RULES.md")
    path = (
        bundled
        if bundled.is_file()
        else Path(__file__).parents[2] / "RULES.md"
    )
    text = path.read_text(encoding="utf-8")
    english, marker, german = text.partition("# Deutsche Version")
    if not marker:
        raise ValueError("RULES.md is missing its German section.")
    return (
        english.rstrip().removesuffix("---").rstrip()
        if language == "en"
        else marker + german
    )
