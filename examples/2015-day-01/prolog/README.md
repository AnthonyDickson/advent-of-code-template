# Advent of Code - Prolog

A [SWI-Prolog](https://www.swi-prolog.org/) template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#prolog` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides SWI-Prolog together with `plunit` (the test framework) and `library(readutil)`, so `just test`
needs no external dependency and nothing has to be downloaded on the first run.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```

- Run the program:

  ```shell
  just run
  ```

- Build a standalone executable at `./aoc`, then run it:

  ```shell
  just build
  ./aoc
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

## Layout

- `src/aoc.pl` holds `solve_part_one/2` and `solve_part_two/2`, the two predicates to implement. Each takes the whole
  puzzle input as a string and unifies its second argument with the answer.
- `src/main.pl` reads `input.txt` and prints both answers.
- `tests/aoc_tests.pl` holds the `plunit` tests that `just test` runs.
