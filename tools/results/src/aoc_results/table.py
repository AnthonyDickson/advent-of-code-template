"""Read and update the results table in ``RESULTS.md``."""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

RESULTS_FILENAME = "RESULTS.md"
COLUMNS = (
    "Day (Part)",
    "Language",
    "Baseline Time",
    "Total Time",
    "Solution Time",
    "Peak RAM (KiB)",
    "Lines",
)
ALIGNMENTS = ("left", "left", "right", "right", "right", "right", "right")
PARTS = ("1", "2", "both")
PART_LABELS = {"1": "1", "2": "2", "both": "Both"}
PART_ORDER = {"1": 0, "2": 1, "Both": 2}

DAY_CELL = re.compile(r"^(?P<day>\d+)\s*\((?P<part>[^)]+)\)$")
ALIGNMENT_CELL = re.compile(r":?-{2,}:?")

DEFAULT_PREAMBLE = (
    "# Results",
    "",
    "Times are recorded with `hyperfine --warmup 3` and rounded to the nearest whole number.",
    "The baseline is the untouched template run on the same input, so the solution time is the",
    "total time minus the baseline. Peak RAM is the maximum resident set size from GNU `time -v`.",
    "Lines are the code lines `tokei` counts in the solution folder, with test files and the",
    "templates' build and project files left out.",
    "",
)

LANGUAGE_NAMES = {
    "clojure": "Clojure",
    "common-lisp": "Common Lisp",
    "elixir": "Elixir",
    "fsharp": "F#",
    "gleam": "Gleam",
    "go": "Go",
    "haskell": "Haskell",
    "lean4": "Lean 4",
    "nushell": "Nushell",
    "ocaml": "OCaml",
    "odin": "Odin",
    "prolog": "Prolog",
    "python": "Python",
    "roc": "Roc",
    "rust": "Rust",
    "scala": "Scala",
    "shakespeare": "Shakespeare",
    "sql": "SQL",
    "typescript": "TypeScript",
    "typst": "Typst",
    "zig": "Zig",
}

# Vendored monochrome icons, from Simple Icons (CC0). Prolog, roc and shakespeare have no icon
# in any set we can vendor, so they fall back to a plain name; SQL shows DuckDB's icon because the
# template's solutions are DuckDB macros. See `icons/README.md` for the provenance of every file.
LANGUAGE_ICONS = {
    "clojure": "clojure.svg",
    "common-lisp": "common-lisp.svg",
    "elixir": "elixir.svg",
    "fsharp": "fsharp.svg",
    "gleam": "gleam.svg",
    "go": "go.svg",
    "haskell": "haskell.svg",
    "nushell": "nushell.svg",
    "ocaml": "ocaml.svg",
    "odin": "odin.svg",
    "python": "python.svg",
    "rust": "rust.svg",
    "scala": "scala.svg",
    "sql": "duckdb.svg",
    "typescript": "typescript.svg",
    "typst": "typst.svg",
    "zig": "zig.svg",
}

ICON_DIR = Path(__file__).resolve().parents[2] / "icons"


@dataclass(frozen=True)
class Row:
    """One benchmark result, one line of the table."""

    language: str
    day: int
    part: str
    baseline_us: float
    total_us: float
    peak_ram_kib: int
    lines: int

    @property
    def solution_us(self) -> float:
        return max(self.total_us - self.baseline_us, 0.0)

    def cells(self, icon_prefix: str | None = None) -> list[str]:
        return [
            f"{self.day} ({self.part})",
            language_label(self.language, icon_prefix),
            format_microseconds(self.baseline_us),
            format_microseconds(self.total_us),
            format_microseconds(self.solution_us),
            f"{self.peak_ram_kib:,}",
            f"{self.lines:,}",
        ]


def language_label(language: str, icon_prefix: str | None = None) -> str:
    """The language's name, preceded by its vendored icon when one exists."""
    name = LANGUAGE_NAMES.get(language, language.replace("-", " ").title())
    icon = LANGUAGE_ICONS.get(language)
    if icon is None or icon_prefix is None:
        return name
    return f"![{name}]({icon_prefix}/{icon})"


def relative_icon_prefix(path: Path) -> str:
    """The icon directory as a link target from the markdown file at *path*."""
    return Path(os.path.relpath(ICON_DIR, path.parent)).as_posix()


def format_microseconds(value: float) -> str:
    """Round to whole microseconds and group the thousands, as the table's other rows do."""
    return f"{round(value):,} µs"


def upsert(path: Path, row: Row, *, icon_prefix: str | None = None) -> None:
    """Add *row* to the table in *path*, replacing any row for the same day and part."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    preamble, rows = _read(lines)
    added = row.cells(icon_prefix)
    rows = [existing for existing in rows if _key(existing) != _key(added)]
    rows.append(added)
    rows.sort(key=_key)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_render(preamble, rows), encoding="utf-8")


def _read(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """Split *lines* into the text before the table and the table's data rows."""
    start = next((index for index, line in enumerate(lines) if line.lstrip().startswith("|")), None)
    if start is None:
        return (lines or list(DEFAULT_PREAMBLE)), []

    end = start
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    block = [_cells(line) for line in lines[start:end]]
    return lines[:start], [row for row in block[1:] if not _is_alignment(row)]


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_alignment(row: list[str]) -> bool:
    return bool(row) and all(ALIGNMENT_CELL.fullmatch(cell) for cell in row)


def _key(row: list[str]) -> tuple[int, int]:
    match = DAY_CELL.match(row[0]) if row else None
    if match is None:
        return (0, len(PART_ORDER))
    return (int(match["day"]), PART_ORDER.get(match["part"], len(PART_ORDER)))


def _render(preamble: list[str], rows: list[list[str]]) -> str:
    """Write *rows* under the header, leaving the column padding to the markdown formatter."""
    width = len(COLUMNS)
    normalized = [[*row[:width], *([""] * max(width - len(row), 0))] for row in rows]
    table = [
        _row(COLUMNS),
        _row(":---" if align == "left" else "---:" for align in ALIGNMENTS),
        *(_row(row) for row in normalized),
    ]

    before = list(preamble)
    while before and not before[-1]:
        before.pop()
    document = [*before, "", *table] if before else table
    return "\n".join(document) + "\n"


def _row(cells: Iterable[str]) -> str:
    return "| " + " | ".join(cells) + " |"
