# Advent of Code - Common Lisp

A Common Lisp template for Advent of Code, built with [SBCL](https://www.sbcl.org/) and
[ASDF](https://asdf.common-lisp.dev/).

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to run this project. If you have
`nix`, run `nix develop .#common-lisp` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides an SBCL that can already load `rove` (the test framework), so nothing has to be downloaded on the
first run.

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

- `src/aoc.lisp` holds `solve-part-one` and `solve-part-two`, the two functions to implement.
- `src/main.lisp` reads `input.txt` and prints both answers.
- `tests/aoc-test.lisp` holds the `rove` tests that `just test` runs.
