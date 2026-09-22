# Advent of Code - Odin

An [Odin](https://odin-lang.org/) template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#odin` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

## Useful Commands

- Run the tests for the solution package:

  ```shell
  just test
  ```

- Run the program:

  ```shell
  just run
  ```

- Build an executable at `./aoc`, then run it:

  ```shell
  just build
  ./aoc
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

## Layout

- `src/aoc/aoc.odin` holds `solve_part_one` and `solve_part_two`, the two procedures to implement.
- `src/main.odin` reads `input.txt` and prints both answers.
- `src/aoc/aoc_test.odin` holds the tests that `just test` runs.
