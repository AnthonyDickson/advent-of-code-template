"""Run a solution's ``just benchmark`` recipe and read hyperfine's JSON export."""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

MICROSECONDS_PER_SECOND = 1_000_000
BYTES_PER_KIB = 1024


class BenchmarkError(Exception):
    """Raised when ``just benchmark`` fails or its results cannot be read."""


@dataclass(frozen=True)
class Benchmark:
    """What one ``just benchmark`` run reports."""

    total_us: float
    peak_ram_kib: int


def run(directory: Path) -> Benchmark:
    """Run ``just benchmark`` in *directory* and read the mean time and peak RAM.

    Every template's recipe forwards its arguments to hyperfine, so the recorder asks it for
    ``--export-json`` rather than scraping the terminal output.
    """
    if not (directory / "justfile").is_file():
        raise BenchmarkError(f"{directory} has no justfile to benchmark")

    with tempfile.TemporaryDirectory() as scratch:
        export = Path(scratch) / "hyperfine.json"
        try:
            completed = subprocess.run(
                ("just", "benchmark", "--export-json", str(export)),
                cwd=directory,
                capture_output=True,
                check=False,
                text=True,
            )
        except FileNotFoundError as error:
            raise BenchmarkError("`just` is not on PATH; run this inside a dev shell") from error

        if completed.returncode != 0:
            output = (completed.stdout + completed.stderr).strip()
            raise BenchmarkError(f"`just benchmark` failed in {directory}:\n{output}")
        if not export.is_file():
            raise BenchmarkError(
                f"`just benchmark` in {directory} wrote no hyperfine JSON; its recipe must pass"
                " its arguments on to hyperfine (`benchmark *args:` ... `hyperfine ... {{args}}`)"
            )
        return parse(export.read_text(encoding="utf-8"))


def parse(export: str) -> Benchmark:
    """Read the mean time and the peak resident set size out of a hyperfine JSON export."""
    try:
        result = json.loads(export)["results"][0]
        mean_seconds = float(result["mean"])
        peak_bytes = max(int(usage) for usage in result["memory_usage_byte"])
    except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as error:
        raise BenchmarkError(f"the hyperfine JSON export could not be read: {error!r}") from error

    return Benchmark(
        total_us=mean_seconds * MICROSECONDS_PER_SECOND,
        peak_ram_kib=round(peak_bytes / BYTES_PER_KIB),
    )
