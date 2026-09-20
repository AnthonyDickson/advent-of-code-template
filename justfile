default:
    @just --list

# Spin the language lottery, then optionally bootstrap the day's solution.
spin *args:
    uv run --directory tools/lottery aoc-lottery {{args}}

# Check the lottery tool.
lottery-test:
    uv run --directory tools/lottery pytest

lottery-lint:
    uv run --directory tools/lottery ruff check

lottery-fmt:
    uv run --directory tools/lottery ruff format

# Move the lottery tool's lockfile to the latest dependency versions.
lottery-update:
    uv --directory tools/lottery lock --upgrade

# Move the nixpkgs and rust-overlay pins in flake.lock to their latest revisions.
update-flake:
    nix flake update

# Bump the dprint plugins pinned in dprint.json.
update-dprint:
    dprint config update

alias lottery := spin
alias pick := spin
