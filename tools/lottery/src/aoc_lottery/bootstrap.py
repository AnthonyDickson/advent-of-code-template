"""Copy a language template into a new solution folder."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from aoc_lottery.config import TEMPLATE_DIRNAME

MIN_YEAR = 2015
LAST_DAY = 25

# Build output and caches that templates gitignore but that may sit in the working tree.
# These lists are only the fallback for when git cannot be asked: normally the skip set is
# derived from the template's own ignore rules, so a new language never needs an entry here
# (see `_ignored_below`).
IGNORED_DIRS = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        ".zig-cache",
        "__pycache__",
        "_build",
        "build",
        "dist-newstyle",
        "node_modules",
        "target",
        "zig-cache",
        "zig-out",
        "zig-pkg",
    }
)
# Puzzle inputs belong to the day being bootstrapped, never to the template.
IGNORED_FILES = frozenset({"input.txt"})
# Compiled binaries (Go builds `cli`) only ever appear at the top level of a template.
IGNORED_TOP_LEVEL = frozenset({"cli"})


class BootstrapError(Exception):
    """Raised when a template cannot be copied."""


@dataclass(frozen=True)
class Bootstrap:
    """The result of copying a template."""

    language: str
    year: int
    day: int
    source: Path
    destination: Path
    copied: tuple[str, ...]

    @property
    def file_count(self) -> int:
        return len(self.copied)


def current_year() -> int:
    """The year to default to when asking for a day number."""
    return datetime.now(tz=UTC).year


def validate_day(day: int) -> int:
    if not 1 <= day <= LAST_DAY:
        raise BootstrapError(f"day must be between 1 and {LAST_DAY}, got {day}")
    return day


def validate_year(year: int) -> int:
    if year < MIN_YEAR:
        raise BootstrapError(f"year must be {MIN_YEAR} or later, got {year}")
    return year


def default_destination(repo: Path, year: int, day: int) -> Path:
    """``<repo>/<year>-day-<dd>``, next to ``template/``."""
    return repo / f"{year}-day-{day:02d}"


def display_path(path: Path, repo: Path) -> str:
    """*path* relative to the repository when possible, otherwise absolute."""
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def bootstrap(
    repo: Path,
    language: str,
    year: int,
    day: int,
    destination: Path | str | None = None,
) -> Bootstrap:
    """Copy ``template/<language>`` into a new folder for one day's puzzle."""
    repo = repo.expanduser().resolve()
    validate_year(year)
    validate_day(day)

    source = repo / TEMPLATE_DIRNAME / language
    if not source.is_dir():
        raise BootstrapError(f"no template for {language!r} in {repo / TEMPLATE_DIRNAME}")

    target = Path(destination).expanduser() if destination else default_destination(repo, year, day)
    if not target.is_absolute():
        target = repo / target
    target = target.resolve()

    if target == source or source in target.parents:
        raise BootstrapError(f"destination {target} is inside the template it would copy")
    if target.exists():
        raise BootstrapError(f"{target} already exists, refusing to overwrite it")

    shutil.copytree(source, target, ignore=_ignore_inside(source, repo))
    copied = tuple(
        sorted(str(path.relative_to(target)) for path in target.rglob("*") if path.is_file())
    )
    return Bootstrap(language, year, day, source, target, copied)


def _ignore_inside(source: Path, repo: Path):
    """Build the copytree filter that skips ignored build output and stale test inputs."""
    ignored = _ignored_below(source, repo)

    def ignore(directory: str, names: list[str]) -> set[str]:
        if ignored is not None:
            parent = Path(directory)
            return {name for name in names if parent / name in ignored}

        top_level = Path(directory) == source
        skipped = {name for name in names if name in IGNORED_DIRS or name in IGNORED_FILES}
        skipped |= {name for name in names if top_level and name in IGNORED_TOP_LEVEL}
        return skipped

    return ignore


def _ignored_below(source: Path, repo: Path) -> frozenset[Path] | None:
    """Everything under *source* that git ignores, or ``None`` when git cannot be asked.

    Every template declares its own build output in a ``.gitignore``, so the template's
    ignore rules are the single source of truth for what must not be copied into a solution
    folder. That also picks up the repository-wide rules, ``**/input.txt`` above all.
    """
    try:
        root = _run_git(repo, "rev-parse", "--show-toplevel").strip()
        listing = _run_git(
            repo,
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
            "--directory",
            "--full-name",
            "-z",
            "--",
            str(source),
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    work_tree = Path(root)
    return frozenset(work_tree / name.rstrip("/") for name in listing.split("\0") if name)


def _run_git(repo: Path, *arguments: str) -> str:
    """Run git in *repo* and return its stdout, raising on a non-zero exit status."""
    completed = subprocess.run(
        ("git", "-C", str(repo), *arguments),
        capture_output=True,
        check=True,
        text=True,
    )
    return completed.stdout
