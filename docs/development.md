# Development and GitHub workflow

This is an independent project. Its `src/`, `tests/`, `pyproject.toml`, `uv.lock`,
and `justfile` layout follows familiar Python conventions. No files, dependencies,
Git remotes, or workflows are shared with other user projects.
The Mahjong calculation rules are defined only by [SPEC.md](../SPEC.md).

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
git commit -m "Set up Mahjong calculator with tests and CI"
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

The pre-existing travel DOCX and older Mahjong cheat-sheet PDF stay on disk but
are excluded from Git. The PDF describes different scoring conventions and is
not the rules reference for this calculator.

## Desktop

`just play` opens the GUI; `just cli` starts the terminal interface.
`just desktop-build` builds the app for this OS. See [desktop.md](desktop.md).
GUI tests use Qt's offscreen platform. Standard-library discovery skips them
when the optional desktop dependencies are not installed.
