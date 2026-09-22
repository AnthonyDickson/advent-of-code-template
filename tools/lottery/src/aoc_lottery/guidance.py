"""Per-language hints and the next steps printed after a template is copied."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from aoc_lottery.bootstrap import Bootstrap, display_path

FALLBACK_SHELL = "fish"


@dataclass(frozen=True)
class Guide:
    """Where the solution goes and what the two entry points are called."""

    entry_point: str
    part_one: str
    part_two: str
    notes: tuple[str, ...] = ()


GUIDES: dict[str, Guide] = {
    "clojure": Guide(
        entry_point="src/aoc.clj",
        part_one="solve-part-one",
        part_two="solve-part-two",
        notes=(
            "The Clojure CLI downloads Clojure and the test runner on the first run, so the first `just test` needs network.",
            "Tests live in `test/aoc_test.clj` and run through the cognitect test runner.",
            "`just build` packages an executable uberjar at `target/aoc.jar`.",
        ),
    ),
    "common-lisp": Guide(
        entry_point="src/aoc.lisp",
        part_one="solve-part-one",
        part_two="solve-part-two",
        notes=(
            "Tests live in `tests/aoc-test.lisp` and run through `rove`, which the dev shell already provides.",
            "`just build` dumps a standalone executable to `./aoc`.",
        ),
    ),
    "elixir": Guide(
        entry_point="lib/aoc.ex",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=(
            "`mix test` also runs the doctests, so keep the `@doc` examples in `lib/aoc.ex` correct.",
        ),
    ),
    "fsharp": Guide(
        entry_point="src/Aoc.fs",
        part_one="solvePartOne",
        part_two="solvePartTwo",
        notes=(
            "Tests live in `tests/AocTests.fs` and run through Expecto (`just test`).",
            "`just fmt` runs `dotnet fantomas`, restored by the dev shell from `.config/dotnet-tools.json`.",
        ),
    ),
    "gleam": Guide(
        entry_point="src/aoc.gleam",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=("Add cases to `test/aoc_test.gleam` to check your types as you go.",),
    ),
    "go": Guide(
        entry_point="aoc/aoc.go",
        part_one="SolvePartOne",
        part_two="SolvePartTwo",
        notes=("The built binary is called `cli` so it does not collide with the `aoc` package.",),
    ),
    "haskell": Guide(
        entry_point="src/Aoc.hs",
        part_one="solvePartOne",
        part_two="solvePartTwo",
        notes=("Tests live in `test/Tests.hs` and `just fmt` runs `ormolu`.",),
    ),
    "ocaml": Guide(
        entry_point="lib/aoc.ml",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=(
            "`Aoc.load_input` returns the input as a `string list` of lines, not a single string.",
        ),
    ),
    "odin": Guide(
        entry_point="src/aoc/aoc.odin",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=(
            "`just test` runs the `@(test)` procedures in `src/aoc/aoc_test.odin` with Odin's built-in test runner.",
            "Test files begin with `#+test`, so they are only compiled by `odin test`, never by `just run` or `just build`.",
            "`just build` compiles a single executable to `./aoc`.",
        ),
    ),
    "python": Guide(
        entry_point="main.py",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=("Tests live in `tests/test_aoc.py`.",),
    ),
    "roc": Guide(
        entry_point="src/Aoc.roc",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=(
            "Roc module names are capitalised, which is why the solution file is `src/Aoc.roc`.",
            "Tests are the `expect` statements in `src/Aoc.roc`; `roc test` runs them without downloading the platform.",
            "Roc keeps going after it reports an error and may still run the program, so `just check` is the way to see type errors on their own.",
            "The first `just run`, `just check` or `just build` downloads the `basic-cli` platform and caches it, so it needs network.",
        ),
    ),
    "rust": Guide(
        entry_point="src/main.rs",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=("Tests are the inline `#[cfg(test)] mod tests` at the bottom of `src/main.rs`.",),
    ),
    "scala": Guide(
        entry_point="src/aoc.scala",
        part_one="solvePartOne",
        part_two="solvePartTwo",
        notes=(
            "Scala CLI fetches the compiler and any libraries on the first run, so the first `just test` needs network.",
            "Tests live in `test/aoc.test.scala` and run through MUnit.",
            "`just build` packages a self-contained executable at `./aoc`.",
        ),
    ),
    "shakespeare": Guide(
        entry_point="src",
        part_one="part_one.spl",
        part_two="part_two.spl",
        notes=(
            "The two parts are separate plays in `src/`, because a play reads its input once and cannot rewind it.",
            "`uv` fetches the interpreter from PyPI into `.venv` on the first `just test` or `just run`, so that run needs network.",
            "Tests live in `tests/test_aoc.py`; `aoc.py` feeds `input.txt` to each play and prints both answers.",
            "SPL has no formatter, so `just fmt` and `just lint` only cover the Python harness.",
        ),
    ),
    "typst": Guide(
        entry_point="src/aoc.typ",
        part_one="solve-part-one",
        part_two="solve-part-two",
        notes=(
            "Typst cannot print, so `main.typ` is the entry point: it reads `input.txt`, renders both answers and publishes them as metadata that `just run` reads back with `typst eval`.",
            "`just run`, `just build`, `just lint` and `just benchmark` compile `main.typ`, which reads `input.txt`, so save the input first; `just test` and `just fmt` need neither.",
            "`while` loops stop after 10,000 iterations and function calls nest at most 80 deep, so long puzzles want `for` loops and explicit stacks.",
        ),
    ),
    "zig": Guide(
        entry_point="src/main.zig",
        part_one="solve_part_one",
        part_two="solve_part_two",
        notes=("`just benchmark` needs the release binary from `just build`.",),
    ),
}


@dataclass(frozen=True)
class Step:
    """One thing left to do before the day is solvable."""

    title: str
    command: str | None = None
    detail: str | None = None


def preferred_shell() -> str:
    """The user's login shell, used in the printed ``nix develop`` command."""
    return Path(os.environ.get("SHELL", "")).name or FALLBACK_SHELL


def guide_for(language: str) -> Guide:
    return GUIDES.get(language, Guide("the template", "solve_part_one", "solve_part_two"))


def bootstrap_steps(plan: Bootstrap, repo: Path, shell: str) -> tuple[Step, ...]:
    """Everything to do once the template has been copied."""
    guide = guide_for(plan.language)
    location = display_path(plan.destination, repo)
    return (
        Step("Open the new folder", command=f"cd {location}"),
        Step(
            f"Enter the {plan.language} dev shell",
            command=f"nix develop .#{plan.language} -c {shell}",
            detail="Run it from anywhere inside this repository; swap the shell for your own.",
        ),
        Step(
            f"Save the {plan.year} day {plan.day} puzzle input",
            detail=f"Save it as `{location}/input.txt` (puzzle inputs are never committed).",
        ),
        Step(
            "Implement both parts",
            detail=f"`{guide.part_one}` and `{guide.part_two}` in `{guide.entry_point}`.",
        ),
        Step("Check the tests that ship with the template", command="just test"),
        Step("Run it against the real input", command="just run"),
        Step(
            "Benchmark it once it passes",
            command="just benchmark",
            detail="Needs the Nix dev shell.",
        ),
    )


def next_steps_markdown(plan: Bootstrap, repo: Path, shell: str) -> str:
    """Render the next steps for the TUI. The heading above this names the folders."""
    lines = [
        f"Copied {plan.file_count} files from `{display_path(plan.source, repo)}`.",
        "",
        "#### Next steps",
        "",
    ]
    for number, step in enumerate(bootstrap_steps(plan, repo, shell), start=1):
        lines += [f"**{number}. {step.title}**", ""]
        if step.command:
            lines += ["```shell", step.command, "```", ""]
        if step.detail:
            lines += [step.detail, ""]

    notes = guide_for(plan.language).notes
    if notes:
        lines += ["#### Good to know", ""]
        lines += [f"- {note}" for note in notes]
        lines += [""]
    return "\n".join(lines)


def plain_steps(plan: Bootstrap, repo: Path, shell: str) -> tuple[str, ...]:
    """Render the next steps for a terminal without the TUI."""
    rendered = []
    for number, step in enumerate(bootstrap_steps(plan, repo, shell), start=1):
        rendered.append(f"{number:>2}. {step.title}")
        if step.command:
            rendered.append(f"    $ {step.command}")
        if step.detail:
            rendered.append(f"    {step.detail}")
    return tuple(rendered)
