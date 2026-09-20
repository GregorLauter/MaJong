<p align="center"><img src="assets/mah_jong_banner.png" width="580" alt="Mah Jong banner"></p>

# Mah Jong

An offline score calculator and settlement tracker for four players, using our
traditional Chinese Mah Jong rules. Enter hand values; the app keeps the totals.

**[Deutsch weiter unten ↓](#deutsch)**

## Download Mah Jong

**Version 0.1.0 · Desktop test release**

| Your computer | Download |
| --- | --- |
| Windows · 64-bit Intel/AMD | [Download for Windows](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-Windows-x64.zip) |
| macOS 13+ · Apple Silicon (M1 or newer) | [Download for Mac](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-macOS-arm64.zip) |
| Linux · 64-bit Intel/AMD · Ubuntu 24.04 build | [Download for Linux](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-Linux-x64.tar.gz) |

Download, extract the archive, then open **Mah Jong**. No Python or terminal is
needed for the Windows/Mac bundles. Linux compatibility depends on your system.
[Opening instructions](docs/downloads.md) · [All releases](https://github.com/GregorLauter/MaJong/releases)

These are test app bundles, not signed installers. macOS/Windows may block or
warn about the unverified publisher. The Mac download does not support Intel Macs.

**[Bilingual rulebook PDF — English first, German below](output/pdf/Mah-Jong-rules.pdf)**
· [Read the rules online](RULES.md)

### Using the calculator

1. Enter four names in initial East/South/West/North order.
2. Enter four hand values and select the winner, then click **Settle hand**.
3. See payments, cumulative totals, seat/Round Winds and hand history.
4. Use **Save game** to continue later, or **Rules / Regeln** for the rulebook.

East rotates automatically. Unsuccessful hands can be recorded without changing
scores or East. Everything stays on your laptop. This is a calculator for your
physical table game, not a playable simulator.

<details>
<summary>Development, tests and builds</summary>

With Python 3.12 and `uv`, from the project folder:

```sh
uv sync --locked --extra desktop --dev
uv run --locked --extra desktop majong-desktop
uv run --locked --extra desktop pytest
```

`just check` runs lint, formatting, types and tests. `just desktop-build` builds
for the current operating system. The existing GitHub workflow builds all three
platforms separately. Publishing requires the manually selected release option.

[Development/API](docs/development.md) · [Platform builds](docs/desktop.md)
· [Release preparation](docs/release.md)

`src/mahjong/` contains the independent scoring/settlement engine and interfaces;
`tests/` contains the automated suite. [SPEC.md](SPEC.md) defines settlement
requirements; [RULES.md](RULES.md) defines our bilingual rulebook.

</details>

---

## Deutsch

Mah Jong ist ein Offline-Punkterechner und Abrechnungshelfer für vier Spieler
nach unseren traditionellen chinesischen Mah Jong-Regeln. Handwerte eingeben;
die App führt die Gesamtstände.

### Mah Jong herunterladen

**Version 0.1.0 · Desktop-Testversion**

| Dein Computer | Download |
| --- | --- |
| Windows · 64-Bit Intel/AMD | [Für Windows herunterladen](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-Windows-x64.zip) |
| macOS 13+ · Apple Silicon (M1 oder neuer) | [Für Mac herunterladen](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-macOS-arm64.zip) |
| Linux · 64-Bit Intel/AMD · Ubuntu-24.04-Build | [Für Linux herunterladen](https://github.com/GregorLauter/MaJong/releases/download/v0.1.0/Mah-Jong-Linux-x64.tar.gz) |

Herunterladen, Archiv entpacken und **Mah Jong** öffnen. Die Windows-/Mac-Pakete
benötigen weder Python noch Terminalkenntnisse. Unter Linux hängt die
Kompatibilität vom System ab. [Anleitung](docs/downloads.md#deutsch)
· [Alle Releases](https://github.com/GregorLauter/MaJong/releases)

Dies sind Testpakete, keine signierten Installer. macOS/Windows können wegen des
ungeprüften Herausgebers warnen oder das Öffnen blockieren. Der Mac-Download
unterstützt keine Intel-Macs.

**[Zweisprachiges Regel-PDF — Englisch zuerst, Deutsch darunter](output/pdf/Mah-Jong-rules.pdf)**
· [Regeln online lesen](RULES.md)

### Den Rechner verwenden

1. Vier Namen in anfänglicher Ost/Süd/West/Nord-Reihenfolge eingeben.
2. Vier Handwerte und den Gewinner auswählen, dann **Settle hand** anklicken.
3. Zahlungen, Gesamtstände, Sitz-/Rundenwinde und Verlauf ansehen.
4. Mit **Save game** speichern; **Rules / Regeln** öffnet das Regelwerk.

Ost wandert automatisch weiter. Erfolglose Hände lassen Punkte und Ost unverändert.
Alles bleibt auf deinem Laptop. Die App rechnet euer Spiel am echten Tisch ab;
sie ist kein spielbarer Simulator.

<details>
<summary>Entwicklung, Tests und Builds</summary>

Mit Python 3.12 und `uv` im Projektordner:

```sh
uv sync --locked --extra desktop --dev
uv run --locked --extra desktop majong-desktop
uv run --locked --extra desktop pytest
```

`just check` prüft Stil, Formatierung, Typen und Tests. `just desktop-build`
erstellt ein Paket für das aktuelle Betriebssystem. Der vorhandene GitHub-Workflow
baut die drei Plattformen getrennt. Veröffentlicht wird nur über die manuell
ausgewählte Release-Option.

[Entwicklung/API](docs/development.md) · [Plattform-Builds](docs/desktop.md)
· [Release-Vorbereitung](docs/release.md) (Englisch)

`src/mahjong/` enthält die unabhängigen Berechnungen und Oberflächen; `tests/`
enthält die Tests. [SPEC.md](SPEC.md) definiert die Abrechnung;
[RULES.md](RULES.md) enthält das zweisprachige Regelwerk.

</details>
