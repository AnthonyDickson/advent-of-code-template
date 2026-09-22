"""Run the two Shakespeare plays on `input.txt` and print one answer per line."""

from __future__ import annotations

import contextlib
import io
import sys
from collections.abc import Iterator
from pathlib import Path

from shakespearelang import Shakespeare

PLAY_DIRECTORY = Path(__file__).parent / "src"
PART_ONE = PLAY_DIRECTORY / "part_one.spl"
PART_TWO = PLAY_DIRECTORY / "part_two.spl"


@contextlib.contextmanager
def _stdin_from(puzzle_input: str) -> Iterator[None]:
    """Make the interpreter's basic input style read from *puzzle_input*."""
    original = sys.stdin
    sys.stdin = io.StringIO(puzzle_input)
    try:
        yield
    finally:
        sys.stdin = original


def run_play(play: Path, puzzle_input: str) -> str:
    """Run *play* with *puzzle_input* on its standard input, returning what it printed.

    A play reads its input once, as a stream, so the two parts are two plays that are
    each given the whole of `input.txt`.
    """
    interpreter = Shakespeare(
        play.read_text(encoding="utf-8"),
        input_style="basic",
        output_style="basic",
    )
    output = io.StringIO()
    with contextlib.redirect_stdout(output), _stdin_from(puzzle_input):
        interpreter.run()
    return output.getvalue()


def solve_part_one(puzzle_input: str) -> int:
    """The answer the part one play prints for *puzzle_input*."""
    return int(run_play(PART_ONE, puzzle_input))


def solve_part_two(puzzle_input: str) -> int:
    """The answer the part two play prints for *puzzle_input*."""
    return int(run_play(PART_TWO, puzzle_input))


def main() -> None:
    puzzle_input = Path("input.txt").read_text(encoding="utf-8")

    print(solve_part_one(puzzle_input))
    print(solve_part_two(puzzle_input))


if __name__ == "__main__":
    main()
