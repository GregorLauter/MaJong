# Rules / Regeln

The complete rulebook lives in **[RULES.md](../RULES.md)**: English first, German
below. Use **Rules / Regeln** inside the calculator to choose either language,
or [download the bilingual PDF](../output/pdf/Mah-Jong-rules.pdf).
[SPEC.md](../SPEC.md) separately defines settlement requirements. The gameplay
instructions describe your physical table game, not features of a simulator.

Das vollständige Regelwerk steht in **[RULES.md](../RULES.md)**: Englisch zuerst,
Deutsch darunter. Über **Rules / Regeln** lässt sich die Sprache im Rechner
wählen. Alternativ: [zweisprachiges PDF herunterladen](../output/pdf/Mah-Jong-rules.pdf).
[SPEC.md](../SPEC.md) definiert die Abrechnung. Die Spielanleitung beschreibt das
Spiel am echten Tisch; die App bleibt ein Punkterechner und Abrechnungshelfer.

## Regenerate the PDF / PDF neu erstellen

From the project folder, with the existing desktop dependencies installed:
Im Projektordner, mit den bereits installierten Desktop-Abhängigkeiten:

```sh
uv run --locked --extra desktop python tools/export_rules_pdf.py
```

Or / oder: `just rules-pdf`.

The export reads `RULES.md` directly, preserves both language sections and starts
German on a fresh page. It uses the existing Qt dependency; no additional PDF
library is needed. Re-export after editing the rules. Older PDF drafts elsewhere
in the folder are not the current rulebook.

Der Export liest `RULES.md` direkt, erhält beide Sprachabschnitte und beginnt
Deutsch auf einer neuen Seite. Er verwendet die vorhandene Qt-Abhängigkeit;
eine zusätzliche PDF-Bibliothek ist nicht nötig. Nach Regeländerungen erneut
exportieren. Ältere PDF-Entwürfe an anderen Stellen sind nicht das aktuelle Regelwerk.
