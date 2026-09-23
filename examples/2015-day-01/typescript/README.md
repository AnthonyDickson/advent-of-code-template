# Advent of Code - TypeScript

A TypeScript template for Advent of Code, built with [Deno](https://deno.com/).

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#typescript` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides Deno, which runs TypeScript directly and type-checks it with `strict` enabled, so nothing has to
be installed to run the solutions. The test suite imports [`@std/assert`](https://jsr.io/@std/assert) from JSR, which
Deno downloads and caches on the first `just test`, so that run needs network.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```

- Type-check the project without running it:

  ```shell
  just check
  ```

- Run the program:

  ```shell
  just run
  ```

- Compile a standalone executable at `./aoc`, then run it:

  ```shell
  just build
  ./aoc
  ```

- Format the project with `deno fmt`, then lint it with `deno lint`:

  ```shell
  just fmt
  just lint
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

## Layout

- `src/aoc.ts` holds `solvePartOne` and `solvePartTwo`, the two functions to implement.
- `src/main.ts` reads `input.txt` and prints both answers.
- `tests/aoc_test.ts` holds the `deno test` tests that `just test` runs.
