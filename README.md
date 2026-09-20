# MaJong

An offline desktop scorekeeper for four-player Chinese Classical Mahjong.
Enter your hand values, choose the winner, and let MaJong settle the table.

A standalone project, with its own source code, Git history, environment, and
builds. It does not connect to or modify any other project.

## Desktop app

- A clean forest-green and ivory interface.
- Four-player setup in East/South/West/North order.
- Round settlement, cumulative scores, and automatic East rotation.
- Selectable round history with original hand values and totals.
- Save and reopen games as portable local JSON files.
- Clear validation errors and prompts before discarding an unsaved game.
- No server, account, or internet connection needed to play.

All rules come from [SPEC.md](SPEC.md). The app settles values entered by the
players; it does not evaluate tiles. The engine remains independent of Qt.

## Run locally

With `uv` and `just` installed, from this folder:

```sh
just setup
just play
```

Without `just`:

```sh
uv sync --locked --extra desktop --dev
uv run --locked --extra desktop majong-desktop
```

Or use a standard Python virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[desktop]'
majong-desktop
```

Python 3.12 is recommended for desktop development. The engine supports Python
3.9+ with no runtime dependencies; the desktop extra installs PySide6.
Windows setup and game instructions are in [the desktop guide](docs/desktop.md).

For the terminal interface, run `just cli`. After installation, `majong`,
`python -m mahjong`, and `python majong.py` are also supported.

## Checks and builds

```sh
just check          # Ruff lint + formatting, mypy, tests and coverage
just test           # Tests only
just fix            # Format and apply safe lint fixes
just build          # Python wheel and source archive
just desktop-build  # Standalone desktop app for this OS
```

The standalone Mac output is `dist/MaJong.app`. Windows and Linux builds produce
an executable and supporting files inside `dist/MaJong/`. Build on each target
OS; receiving laptops do not need Python installed. The initial bundles are
unsigned development builds, not notarized public release installers.

GitHub Actions checks pushes and pull requests. The manually dispatched
**Desktop packages** workflow tests and builds Mac ARM64, Windows x64, and Linux
x64 packages. Platform coverage is documented in [the desktop guide](docs/desktop.md).

## Project layout

```text
src/mahjong/
  engine.py        # Rules, settlement, game state, invariants
  storage.py       # Atomic saves and validation by replaying rounds
  gui.py           # Qt desktop interface
  cli.py           # Terminal interface
  assets/          # App icon
  __init__.py
  __main__.py
tests/             # Engine, CLI, storage, and real Qt widget tests
packaging/         # Standalone app build specification and icons
.github/workflows/ # Tests and desktop package builds
docs/              # Development and installation guides
SPEC.md            # Authoritative rules
pyproject.toml     # Package metadata and tool configuration
uv.lock            # Locked dependencies
justfile           # Development commands
```

## Engine API

```python
from mahjong import MahjongGame

game = MahjongGame(['A', 'B', 'C', 'D'])
result = game.play_round({'A': 12, 'B': 24, 'C': 8, 'D': 4}, winner='B')
assert result['changes'] == {'A': -24, 'B': 96, 'C': -28, 'D': -44}
assert game.east == 'B'
```

`calculate_round(scores, winner)` previews changes without committing a round.
`play_round(scores, winner)` validates, verifies round and cumulative zero-sum
invariants, updates East, and returns a history entry. Invalid inputs raise
`ValueError`; invariant failures raise `RuntimeError`. Failed rounds never commit.

`players`, `east`, `east_index`, `east_win_streak`, and `round_number` are read-only
properties. `round_number` counts completed rounds. `totals` and `history` return
independent snapshots. History entries contain `round`, `east`, `winner`,
`scores`, `changes`, `totals`, `next_east`, and the following `east_win_streak`.

See [development](docs/development.md) and [third-party notices](THIRD_PARTY_NOTICES.md).
