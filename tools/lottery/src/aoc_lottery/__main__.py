"""Command line entry point for the lottery."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aoc_lottery.app import LotteryApp
from aoc_lottery.bootstrap import BootstrapError, bootstrap, current_year, display_path
from aoc_lottery.config import ConfigError
from aoc_lottery.guidance import plain_steps
from aoc_lottery.session import Session, build_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aoc-lottery",
        description="Draw a language for today's Advent of Code puzzle and bootstrap its template.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=None,
        help="repository root (defaults to the current directory)",
    )
    parser.add_argument(
        "--config", type=Path, default=None, help="weights file (defaults to lottery.toml)"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="seed the draw for a repeatable result"
    )
    parser.add_argument(
        "--shell", default=None, help="shell used by the printed nix develop command"
    )
    parser.add_argument("--plain", action="store_true", help="draw without the TUI")
    parser.add_argument(
        "--day", type=int, default=None, help="bootstrapped day in --plain mode (1-25)"
    )
    parser.add_argument("--year", type=int, default=None, help="bootstrapped year in --plain mode")
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="destination folder (defaults to <year>-day-<dd> in the repository root)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        session = build_session(
            repo=arguments.repo,
            config=arguments.config,
            seed=arguments.seed,
            shell=arguments.shell,
        )
    except (ConfigError, ValueError) as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2

    if arguments.plain:
        return run_plain(
            session, day=arguments.day, year=arguments.year, destination=arguments.dest
        )

    LotteryApp(session).run()
    return 0


def run_plain(
    session: Session, *, day: int | None, year: int | None, destination: Path | None
) -> int:
    """Print the drawn language, and with ``--day`` copy the template and print the next steps."""
    entry = session.lottery.draw()
    print(entry.language)
    print(
        f"drawn from {len(session.lottery.entries)} templates ({entry.percent:.1f}%)",
        file=sys.stderr,
    )

    if day is None:
        print("add --day <n> to bootstrap the template", file=sys.stderr)
        return 0

    try:
        plan = bootstrap(
            session.repo,
            entry.language,
            year if year is not None else current_year(),
            day,
            destination,
        )
    except BootstrapError as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1

    print(file=sys.stderr)
    print(
        f"copied {display_path(plan.source, session.repo)} to "
        f"{display_path(plan.destination, session.repo)} ({plan.file_count} files)",
        file=sys.stderr,
    )
    print(file=sys.stderr)
    for step in plain_steps(plan, session.repo, session.shell):
        print(step, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
