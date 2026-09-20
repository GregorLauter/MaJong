# List available commands.
default:
    @just --list

# Install the project and development tools in .venv.
setup:
    uv sync --locked --extra desktop --dev

# Run all checks (the same checks as GitHub Actions).
check:
    uv run --locked --extra desktop ruff check src/ tests/ majong.py
    uv run --locked --extra desktop ruff format --check src/ tests/ majong.py
    uv run --locked --extra desktop mypy
    uv run --locked --extra desktop pytest

# Run the test suite with coverage.
test:
    uv run --locked --extra desktop pytest

# Format code and apply safe lint fixes.
fix:
    uv run --locked --extra desktop ruff check --fix src/ tests/ majong.py
    uv run --locked --extra desktop ruff format src/ tests/ majong.py

# Open the desktop app.
play:
    uv run --locked --extra desktop majong-desktop

# Open the terminal calculator.
cli:
    uv run --locked majong

# Build an installable wheel and source archive.
build:
    uv build

# Bundle a standalone app for this operating system.
desktop-build:
    uv run --locked --extra desktop pyinstaller --noconfirm packaging/majong.spec

# Export the bilingual rulebook using the existing Qt dependency.
rules-pdf:
    uv run --locked --extra desktop python tools/export_rules_pdf.py
