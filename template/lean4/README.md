# Advent of Code - Lean 4

A [Lean 4](https://lean-lang.org/) template for Advent of Code, built with
[Lake](https://leanprover.github.io/lean4/doc/).

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#lean4` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides the compiler and Lake together, and `lean-toolchain` names the same version, so `lake` uses the
bundled compiler instead of downloading one.

## Useful Commands

- Build and run the program:

  ```shell
  just run
  ```

- Run tests:

  ```shell
  just test
  ```

- Build the executable:

  ```shell
  just build
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

- Remove the build output:

  ```shell
  just clean
  ```

## Layout

- `Aoc.lean` holds `solvePartOne` and `solvePartTwo`, the two functions to implement.
- `Main.lean` reads `input.txt` and prints both answers, one per line.
- `Tests.lean` runs the example checks and exits non-zero when one fails.
