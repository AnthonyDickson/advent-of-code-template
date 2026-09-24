"""Run a solution's ``just benchmark`` recipe and scrape the numbers it prints."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# hyperfine prints: `  Time (mean ± σ):     790.0 µs ±  20.0 µs    [User: ..., System: ...]`.
HYPERFINE_MEAN = re.compile(
    r"Time \(mean ± σ\):\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>ns|µs|us|ms|s)\b"
)
# GNU `time -v` prints: `\tMaximum resident set size (kbytes): 2268`.
MAX_RESIDENT_SET = re.compile(r"Maximum resident set size \(kbytes\):\s*(?P<value>\d+)")
MICROSECONDS_PER_UNIT = {"ns": 1e-3, "µs": 1.0, "us": 1.0, "ms": 1e3, "s": 1e6}


class BenchmarkError(Exception):
    """Raised when ``just benchmark`` fails or its output cannot be read."""


@dataclass(frozen=True)
class Benchmark:
    """What one ``just benchmark`` run reports."""

    total_us: float
    peak_ram_kib: int


def run(directory: Path) -> Benchmark:
    """Run ``just benchmark`` in *directory* and scrape the mean time and peak RAM."""
    if not (directory / "justfile").is_file():
        raise BenchmarkError(f"{directory} has no justfile to benchmark")
    try:
        completed = subprocess.run(
            ("just", "benchmark"), cwd=directory, capture_output=True, check=False, text=True
        )
    except FileNotFoundError as error:
        raise BenchmarkError("`just` is not on PATH; run this inside a dev shell") from error

    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise BenchmarkError(f"`just benchmark` failed in {directory}:\n{output.strip()}")
    return parse(output)


def parse(output: str) -> Benchmark:
    """Read the hyperfine mean and the GNU time peak RSS out of a benchmark's output."""
    mean = HYPERFINE_MEAN.search(output)
    resident = MAX_RESIDENT_SET.search(output)
    if mean is None:
        raise BenchmarkError("the benchmark output has no hyperfine mean time")
    if resident is None:
        raise BenchmarkError("the benchmark output has no peak resident set size")

    return Benchmark(
        total_us=float(mean["value"]) * MICROSECONDS_PER_UNIT[mean["unit"]],
        peak_ram_kib=int(resident["value"]),
    )
