# Advent of Code - Nushell

A [Nushell](https://www.nushell.sh/) template for Advent of Code. Nushell is a shell whose values are structured data,
so `main.nu` reads `input.txt` and prints both answers, and everything else is a pipeline over that string.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#nushell` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides Nushell. Its language server is built in (`nu --lsp`), so there is no separate package for it,
and nothing is downloaded on the first run. Nushell's formatter, `nufmt`, is not wired in: it rewrites valid code into
broken code, so formatting is left to hand editing.

## Useful Commands

- Check both solutions against the examples from the puzzle statement:

  ```shell
  just test
  ```

- Print both answers, one per line:

  ```shell
  just run
  ```

- Parse and type-check the entry point, including its imports:

  ```shell
  just build
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

`just run` reads `input.txt`, so save the puzzle input first. `just test` and `just build` do not need it.

## Layout

- `src/aoc.nu` holds `solve-part-one` and `solve-part-two`, the two functions to implement.
- `main.nu` reads `input.txt` and prints both answers.
- `tests/test_aoc.nu` holds the example cases that `just test` runs.

## Writing a solution

`open --raw input.txt` gives the whole puzzle input as one string. From there the pipeline commands do the work: `split
chars` and `lines` turn it into a list, `parse` pulls out numbers and `where`, `each`, `reduce` and `group-by` walk over
it. `math sum`, `math max` and friends collapse a list of numbers, and `par-each` runs the same pipeline across threads
when a puzzle is slow.

Two conventions follow from the tooling:

- Commands (`def` and `export def`) are kebab-case, which is why the solutions are `solve-part-one` and
  `solve-part-two`, and flow between them is spelled `solve-part-one` rather than `solve_part_one`.
- Variables and parameters are snake_case. `let` binds once; `mut` is what makes a binding assignable, and both `for`
  and `while` need the variables they update to be declared with `mut`.

### Getting the answers out

A Nushell script is run by naming it: `nu main.nu` calls the file's `main` command, and `main` is what reads the input
and `print`s each answer on its own line. Because `print` writes a plain line, the two answers go to stdout exactly as
the CLI contract expects, with no table or colouring wrapping them.

`just build` does not produce a binary, because Nushell has no compiler: it runs `nu --no-config-file --commands 'source
main.nu'` instead, which parses and type-checks `main.nu` and everything it imports without executing the solution. The
`nothing -> int` return type on each solution is what makes that check catch a solution that stops returning an integer.

### Tests

`tests/test_aoc.nu` is a script, not a module: `just test` runs it, and each case is an `assert equal` from the standard
library's `std/assert`. Assertions abort on the first failure and name the input they were given, so a run that prints
`all N examples passed` is a run where every case held. Nushell ships no test framework that discovers tests, so the
tables at the top of the file are the list of cases.

## Notes

- Nushell has no linter and no formatter this template trusts, so there is no `just fmt` or `just lint`; the recipes are
  `test`, `run`, `build` and `benchmark`.
- `nu` starts a REPL with no arguments and `nu src/aoc.nu` runs a file, which is a quick way to try a pipeline before
  wiring it into a solution.
