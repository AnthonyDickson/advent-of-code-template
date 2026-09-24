"""Command line entry point for recording a solution's benchmark times."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from aoc_results import benchmark, repository, table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aoc-results",
        description="Benchmark a solution and add its times to the RESULTS.md table.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="solution folder with input.txt and the template's justfile",
    )
    parser.add_argument(
        "--repo", type=Path, default=None, help="repository root, instead of searching upwards"
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help=f"markdown file to update (defaults to <repo>/{table.RESULTS_FILENAME})",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="template the folder was copied from (defaults to detecting it)",
    )
    parser.add_argument(
        "--day", type=int, default=None, help="puzzle day (defaults to the folder name)"
    )
    parser.add_argument(
        "--part",
        choices=table.PARTS,
        default="both",
        help="which part the row covers (defaults to both)",
    )
    parser.add_argument(
        "--baseline",
        type=float,
        default=None,
        metavar="US",
        help="baseline in microseconds, instead of benchmarking the template",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="puzzle input (defaults to <folder>/input.txt)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        record(arguments)
    except (benchmark.BenchmarkError, repository.RepositoryError, OSError) as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    return 0


def record(arguments: argparse.Namespace) -> None:
    solution = arguments.folder.expanduser().resolve()
    if not solution.is_dir():
        raise repository.RepositoryError(f"{solution} is not a folder")

    repo = (arguments.repo or repository.discover(solution)).expanduser().resolve()
    if solution == repo or repo / repository.TEMPLATE_DIRNAME in solution.parents:
        raise repository.RepositoryError(f"{solution} is not a solution folder")

    language = arguments.language or repository.detect_language(repo, solution)
    day = arguments.day if arguments.day is not None else repository.detect_day(solution)
    input_path = (arguments.input or solution / "input.txt").expanduser().resolve()

    measured = benchmark.run(solution)
    if arguments.baseline is not None:
        baseline_us = arguments.baseline
    else:
        baseline_us = measure_baseline(repo, language, input_path)

    row = table.Row(
        language=language,
        day=day,
        part=table.PART_LABELS[arguments.part],
        baseline_us=baseline_us,
        total_us=measured.total_us,
        peak_ram_kib=measured.peak_ram_kib,
    )
    destination = (arguments.file or repo / table.RESULTS_FILENAME).expanduser().resolve()
    table.upsert(destination, row, icon_prefix=table.relative_icon_prefix(destination))

    print(
        f"{row.day} ({row.part}) {row.language}: "
        f"{table.format_microseconds(row.total_us)} total, "
        f"{table.format_microseconds(row.solution_us)} solution, "
        f"{row.peak_ram_kib:,} KiB peak"
    )
    print(f"recorded in {destination}")


def measure_baseline(repo: Path, language: str, input_path: Path) -> float:
    """Benchmark the untouched template on the same input, to subtract start-up and parsing."""
    template = repo / repository.TEMPLATE_DIRNAME / language
    if not template.is_dir():
        raise repository.RepositoryError(
            f"no template for {language!r} in {repo / repository.TEMPLATE_DIRNAME}"
        )
    if not input_path.is_file():
        raise repository.RepositoryError(
            f"{input_path} does not exist; save the puzzle input or pass --baseline"
        )

    # The template is a runnable dev project and its own `.gitignore` covers the input and any
    # build output, so it can be benchmarked in place instead of in a throwaway copy.
    saved_input = template / "input.txt"
    shutil.copyfile(input_path, saved_input)
    try:
        return benchmark.run(template).total_us
    finally:
        saved_input.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
