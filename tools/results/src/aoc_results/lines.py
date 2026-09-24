"""Count a solution's application code lines with ``tokei``, leaving tests out."""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Iterator
from pathlib import Path

# Languages tokei recognises that are not the solution itself: the build recipes, project
# metadata and documentation every template ships. Everything else it counts is code, which
# keeps languages tokei maps to an unexpected entry (Prolog source is read as Perl, because
# tokei gives `.pl` to Perl) instead of silently dropping them.
NON_CODE_LANGUAGES = frozenset(
    {"Cabal", "Edn", "JSON", "Just", "MSBuild", "Markdown", "TOML", "XML", "YAML"}
)

# Test code lives in a `test/` or `tests/` directory, or in a file whose name has `test` as a
# word of its own: `test_aoc.py`, `aoc_test.go`, `aoc-test.lisp`, `aoc.test.scala`.
TEST_DIRECTORIES = frozenset({"spec", "specs", "test", "tests"})
TEST_NAME = re.compile(r"(?:^|[._-])tests?(?:[._-]|$)", re.IGNORECASE)


class LinesError(Exception):
    """Raised when ``tokei`` is missing or its output cannot be read."""


def count(directory: Path) -> int:
    """The application code lines ``tokei`` counts in *directory*, tests excluded."""
    total = 0
    for language, path, code in _records(_run_tokei(directory)):
        if language in NON_CODE_LANGUAGES:
            continue
        if is_test_file(_relative(directory, path)):
            continue
        total += code
    return total


def is_test_file(path: Path) -> bool:
    """Whether *path*, relative to the solution root, is test code rather than application code."""
    if any(part.lower() in TEST_DIRECTORIES for part in path.parts[:-1]):
        return True
    return bool(TEST_NAME.search(path.name))


def _run_tokei(directory: Path) -> str:
    """Run tokei over *directory* and return its streaming JSON, one record per file."""
    try:
        completed = subprocess.run(
            ("tokei", "--streaming", "json", str(directory)),
            capture_output=True,
            check=False,
            text=True,
        )
    except FileNotFoundError as error:
        raise LinesError("`tokei` is not on PATH; run this inside a dev shell") from error

    if completed.returncode != 0:
        raise LinesError(f"`tokei` failed in {directory}:\n{completed.stderr.strip()}")
    return completed.stdout


def _records(output: str) -> Iterator[tuple[str, Path, int]]:
    """Read the language, path and code line count from every record tokei printed."""
    for line in output.splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            path = record["stats"]["name"]
            code = record["stats"]["stats"]["code"]
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise LinesError(f"unexpected tokei output: {line!r}") from error
        yield record["language"], Path(path), int(code)


def _relative(directory: Path, path: Path) -> Path:
    """*path* relative to *directory*, so a parent folder named `test` cannot match."""
    try:
        return path.relative_to(directory)
    except ValueError:
        return path
