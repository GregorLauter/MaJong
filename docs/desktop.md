# Desktop application

MaJong is a local, offline application. It needs no browser, server, login, or
connection to another project. All scoring runs through `mahjong.engine`.

## Start from this source checkout

With `uv` and `just` installed:

```sh
just setup
just play
```

Or use a standard Python virtual environment (Python 3.12 recommended):

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[desktop]'
majong-desktop
```

On Windows, create the environment with `py -3.12 -m venv .venv`, activate it
with `.venv\Scripts\Activate.ps1`, then use the same pip installation and
`majong-desktop` commands. For the terminal interface, use `just cli` or `majong`.

## Playing

1. Enter four names in initial East/South/West/North order.
2. Enter all four hand values (including an explicit `0` where appropriate).
3. Select the winner using their **Won** button.
4. Click **Settle round**. Totals, East, streak, and history update together.
5. Select a history row to see its entered values and cumulative totals.

Invalid input stays on screen for correction; no partial round is committed.
After settlement the entry fields clear, preventing an accidental second click
from charging the same round again. The previous round's changes remain visible.

**Save game** writes completed rounds to a JSON file in a location you choose.
**Open game** validates and reconstructs that game. Opening, starting a new game,
or closing asks what to do with unsaved completed rounds. Partially typed round
inputs are not part of a saved game. Save files work across operating systems.
The app does not write game data elsewhere automatically.

## Build a standalone application

```sh
just desktop-build
```

The output contains Python and Qt, so the receiving laptop does not need Python:

| Build system | Output | How to use |
| --- | --- | --- |
| macOS | `dist/MaJong.app` | Double-click; optionally drag to Applications yourself. |
| Windows | `dist/MaJong/MaJong.exe` | Keep the entire MaJong folder together; open the executable. |
| Linux | `dist/MaJong/MaJong` | Keep the entire MaJong folder together; run the executable. |

Build on the OS and architecture you intend to distribute to. A Mac build is
not a Windows executable. The GitHub **Desktop packages** workflow builds
macOS ARM64, Windows x64, and Ubuntu 24.04 x64 bundles when manually dispatched.
It runs tests and a startup check before uploading downloadable artifacts.
Intel Macs can build from source on an Intel Mac; an Intel Mac bundle is not
included in the initial workflow. Linux distribution/library compatibility
still matters; this is not a universal binary for every laptop and OS version.
The locked Qt Mac wheels require macOS 13 or newer.

The initial bundles are development builds, without Apple Developer notarization
or a Windows publisher certificate. They are not yet signed public release
installers. See [Qt supported platforms](https://doc.qt.io/qt-6/supported-platforms.html)
and [PyInstaller packaging](https://pyinstaller.org/en/stable/operating-mode.html)
for platform details. Third-party notices and dependency license metadata are
included in the bundles.

## Project isolation

- Code, `.git`, `.venv`, builds, tests, and configuration belong to this folder.
- No other project's files, Git remotes, environment, or settings are modified.
- `uv` may use its normal shared download cache; installed packages remain in
  this project's `.venv`.
- No global Python packages or system-wide application installation are needed.
- Existing personal documents and saved `*.majong.json` games are ignored by Git.
- GitHub publishing targets only the separate `GregorLauter/MaJong` repository.
