import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mahjong.rules import rules_text


class RulesTests(unittest.TestCase):
    def test_actual_bilingual_rulebook(self):
        english, german = rules_text("en"), rules_text("de")
        self.assertIn("## 32. Source of Truth", english)
        self.assertIn("## 32. Maßgebliche Regeln", german)
        self.assertNotIn("# Deutsche Version", english)
        self.assertTrue(german.startswith("# Deutsche Version"))
        self.assertNotIn("## 1. Scope", german)
        self.assertIn("Concealed / Extended", english)

    def test_bundled_rules_and_invalid_language_or_document(self):
        with tempfile.TemporaryDirectory() as directory:
            module = Path(directory) / "rules.py"
            rulebook = module.with_name("RULES.md")
            rulebook.write_text(
                "English\n---\n\n# Deutsche Version\nDeutsch", encoding="utf-8"
            )
            with patch("mahjong.rules.__file__", str(module)):
                self.assertEqual(rules_text("en"), "English")
                self.assertIn("Deutsch", rules_text("de"))
                rulebook.write_text("Missing translation", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "German"):
                    rules_text()
        with self.assertRaisesRegex(ValueError, "language"):
            rules_text("xx")
