"""Export RULES.md using the existing desktop dependency, without extra packages.

Run from the repository: .venv/bin/python tools/export_rules_pdf.py
"""

import os
import re
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QRectF, Qt  # noqa: E402
from PySide6.QtGui import (  # noqa: E402
    QColor,
    QFont,
    QPageSize,
    QPainter,
    QPdfWriter,
    QTextDocument,
)
from PySide6.QtWidgets import QApplication  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Mah-Jong-rules.pdf"
STYLE = """
body { color: #203e35; }
h1 { color: #173e34; font-size: 23pt; margin-bottom: 16px; }
h2 { color: #173e34; font-size: 15pt; margin-top: 17px; margin-bottom: 8px; }
h3 { font-size: 11pt; margin-top: 10px; margin-bottom: 5px; }
p, li { margin-top: 4px; margin-bottom: 6px; }
table { border-collapse: collapse; margin-top: 8px; margin-bottom: 10px; }
th { background-color: #e7eddf; }
td, th { padding: 6px; border: 1px solid #b9c5b5; }
"""


def main() -> None:
    app = QApplication.instance() or QApplication([])
    source = (ROOT / "RULES.md").read_text(encoding="utf-8")
    english, marker, german = source.partition("# Deutsche Version")
    if not marker:
        raise ValueError("RULES.md is missing its German section.")
    languages = [
        ("English", english.rstrip().removesuffix("---").rstrip()),
        ("Deutsch", marker + german),
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    writer = QPdfWriter(str(OUTPUT))
    writer.setResolution(72)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setTitle("MahJong - Rules / Regeln")
    writer.setCreator("MahJong rulebook export from RULES.md")
    width, height = writer.width(), writer.height()
    margin = 38
    content_width = width - 2 * margin
    content_height = height - 2 * margin - 24
    pages: list[tuple[str, list[tuple[float, QTextDocument]]]] = []
    for language, markdown in languages:
        items: list[tuple[float, QTextDocument]] = []
        y = 0.0
        pending = ""
        # Numbered sections are small enough to keep whole, including tables.
        # Section headings without prose belong with the following section.
        for part in re.split(r"(?m)(?=^#{1,2} )", markdown):
            if not part.strip():
                continue
            if "\n" not in part.strip():
                pending += part
                continue
            document = QTextDocument()
            document.documentLayout().setPaintDevice(writer)
            document.setDefaultFont(QFont("Arial", 10))
            document.setDefaultStyleSheet(STYLE)
            document.setMarkdown(pending + part)
            pending = ""
            document.setHtml(document.toHtml())
            document.setDocumentMargin(0)
            document.setTextWidth(content_width)
            size = document.size().height()
            if size > content_height:
                raise ValueError(
                    "A rule section exceeds one PDF page; adjust layout."
                )
            if items and y + size > content_height:
                pages.append((language, items))
                items = []
                y = 0.0
            items.append((y, document))
            y += size + 12
        if pending:
            raise ValueError("The rulebook ends with an empty heading.")
        if items:
            pages.append((language, items))
    total = len(pages)
    painter = QPainter(writer)
    for number, (language, items) in enumerate(pages, 1):
        if number > 1:
            writer.newPage()
        painter.setPen(QColor("#526659"))
        painter.setFont(QFont("Arial", 9))
        painter.drawText(margin, 18, f"MahJong  |  {language}")
        painter.drawText(
            QRectF(margin, height - 23, content_width, 18),
            Qt.AlignmentFlag.AlignRight,
            f"{number} / {total}",
        )
        for y, document in items:
            painter.save()
            painter.translate(margin, margin + y)
            document.drawContents(painter)
            painter.restore()
    painter.end()
    print(f"Created {OUTPUT} ({total} pages)")
    del app


if __name__ == "__main__":
    main()
