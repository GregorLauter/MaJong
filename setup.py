"""Bundle the canonical rulebook and supplied artwork without manual copies."""

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWithRules(build_py):
    def run(self):
        super().run()
        self.copy_file(
            "RULES.md", str(Path(self.build_lib) / "mahjong" / "RULES.md")
        )

        for name in ("mah_jong_banner.png", "mah_jong_icon.png"):
            self.copy_file(
                str(Path("assets") / name),
                str(Path(self.build_lib) / "mahjong" / "assets" / name),
            )


setup(cmdclass={"build_py": BuildWithRules})
