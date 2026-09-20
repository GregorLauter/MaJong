# Development and GitHub workflow

This is an independent project. Its `src/`, `tests/`, `pyproject.toml`, `uv.lock`,
and `justfile` layout follows familiar Python conventions. No files, dependencies,
Git remotes, or workflows are shared with other user projects.
Settlement requirements come from [SPEC.md](../SPEC.md); gameplay and hand
scoring come from the bilingual [RULES.md](../RULES.md).

## Everyday development

Install `uv` and `just` if needed, then run these commands from the repository:

```sh
just setup
just check
just play
```

`just setup` installs the package in editable mode in `.venv` using `uv.lock`.
Edits to `src/mahjong/` take effect immediately. The engine needs no runtime dependencies; the desktop extra installs Qt. Development tools are Ruff, mypy, pytest, and pytest-cov. The existing
unittest test cases also run under pytest, so both test runners remain usable.

`just check` checks lint, formatting, types, and tests with at least 95% coverage.
Use `just fix` to format code and apply safe lint fixes, `just test` for tests
alone, and `just build` to build a wheel and source archive under `dist/`.

Equivalent commands without `just`:

```sh
uv sync --locked --extra desktop --dev
uv run --locked --extra desktop ruff check src/ tests/ majong.py
uv run --locked --extra desktop ruff format --check src/ tests/ majong.py
uv run --locked --extra desktop mypy
uv run --locked --extra desktop pytest
uv run --locked --extra desktop majong-desktop
```

To deliberately update dependencies, run `uv lock --upgrade`, then `just setup`
and `just check`. Commit both `pyproject.toml` and `uv.lock` when they change.

## Local work and GitHub

This folder is the working copy. Git records local snapshots (commits); pushing
sends those commits to the GitHub repository. Continue editing this same folder
after connecting it to GitHub. No second local project or manual file upload is
needed.

After initializing Git and making the first commit, use a branch for a change:

```sh
git switch -c feature/describe-the-change
# Edit code and add or update tests.
just check
git add <the-files-you-changed>
git commit -m "Describe the change"
git push -u origin HEAD
```

Then open a pull request on GitHub. GitHub Actions runs lint, format, type, test,
and build checks on Python 3.12, plus the unittest suite against the installed
package on Python 3.9, 3.10, 3.11, 3.13, and 3.14. These checks are configured for
pushes and pull requests; they can only run on GitHub after the repository is
published. The local command is `just check`.

## First publication (when ready)

If Git has not yet been initialized, run locally:

```sh
git init -b main
git add .gitignore .gitattributes .github README.md SPEC.md docs pyproject.toml uv.lock justfile MANIFEST.in src tests majong.py
git commit -m "Set up Mah Jong calculator with tests and CI"
```

Choose the repository name and whether it should be public or private. Create
an **empty** GitHub repository (without a generated README, license, or
.gitignore), then use its actual clone URL:

```sh
git remote add origin <repository-clone-url>
git push -u origin main
```

Authenticate using your own GitHub login or SSH setup; credentials do not belong
in this repository. No GitHub remote is assumed by the project configuration.
Choose a license before distributing the project for others to reuse; this
setup deliberately does not assign one on your behalf.

## Scope of the setup

- Keep engine runtime dependencies empty and use a static version (`0.1.0`) because the
  calculator currently needs neither scientific libraries nor tag-based releases.
- Keep Python 3.9+ compatibility; local development can use your installed Python.
- Use a focused Ruff rule set rather than every rule, to keep checks useful for
  this small codebase.
- Keep documentation in Markdown; no Sphinx or Read the Docs service is needed.
- Build packages for verification, with no automatic PyPI publishing workflow.
- Use `main`, matching this machine's Git default. The branch name does not affect
  the application or its tests.

The pre-existing travel DOCX and older Mah Jong cheat-sheet PDF stay on disk but
are excluded from Git. The PDF describes different scoring conventions and is
not the rules reference for this calculator.

## Desktop

`just play` opens the GUI; `just cli` starts the terminal interface.
`just desktop-build` builds the app for this OS. See [desktop.md](desktop.md).
GUI tests use Qt's offscreen platform. Standard-library discovery skips them
when the optional desktop dependencies are not installed.

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
properties. `round_number` is a legacy API name: it counts recorded hands, including
unsuccessful hands. A whole Round is tracked separately by `round_wind` and
`completed_rounds`. `totals` and `history` return
independent snapshots. History entries contain `round`, `east`, `winner`,
`scores`, `changes`, `totals`, `next_east`, and the following `east_win_streak`.


## Winds, restarts and completion

`players` is the fixed counterclockwise physical seating order; `initial_east`
is its first player. Determine the initial Winds at the table before entering
names. `seat_winds` maps every player to their current `Wind`. `round_wind`
progresses East, South, West, North whenever East returns to `initial_east`.
After the fourth circuit, `game_over` is true and further hands are rejected.

`restart_hand()` records an unsuccessful hand without changing totals, Winds or
the East streak. The table determines when fewer than eight tiles remain; the
app does not simulate wall draws. History adds `kind`, `seat_winds`, `round_wind`,
`next_round_wind`, `round_completed` and `game_over`. All snapshots are independent.
A restart has `winner=None`, empty `scores` and zero `changes`.

Save format 2 records both successful and unsuccessful hands and reconstructs
all state through engine replay. Format 1 is still accepted, but any saved hand
after the North circuit is rejected with an error. Nothing is silently dropped.

## Hand-scoring API

```python
from mahjong.scoring import Hand, Meld, MeldKind, Suit, Tile, score_hand

# Explicitly arranged hand: a Chow's tile denotes the lowest of three tiles.
hand = Hand(
    melds=tuple(Meld(MeldKind.CHOW, Tile(Suit.BAMBOO, n))
                for n in (1, 2, 4, 7)),
    pair=Tile(Suit.CIRCLES, 5),
)
score = score_hand(hand, seat_wind=game.seat_winds['B'],
                   round_wind=game.round_wind, winner=True)
assert score.ordinary_base == 0
assert score.mahjong_points == 20
assert score.zero_base_bonus == 2
assert score.base_points == score.final_value == 22
assert score.doubles == 0
```

`Exposure` distinguishes exposed, concealed and extended melds. `Dragon` names
honour values; `BonusTile(BonusKind.FLOWER, 1)` describes a numbered bonus tile.
Supply at most one scoring pair; other unscored material belongs in `loose_tiles`.
A winner requires four melds, a pair and no loose material. The API validates
component types, tile values, duplicate bonus tiles and the four-copy tile limit.
It accepts declared arrangements; it does not search for a winning arrangement,
judge claims, or validate the entire table's tile inventory.

Calculate **all four** hand values using the Winds before settlement, then pass
those values to `play_round`. Hand scoring never applies East's payment multiplier.
The GUI accepts final values. This remains a calculator; virtual hands, dealing,
wall simulation and playable meld logic are outside its scope.

## Single rulebook in packages

`setup.py` copies the root `RULES.md` into wheel builds; `MANIFEST.in` includes
it in source archives. The PyInstaller spec bundles that same file. Source runs
read the root document. `rules.py` splits its existing language sections, and
the Qt dialog renders Markdown without a separately maintained rules text.
PDF export preparation is documented in [rules.md](rules.md).
