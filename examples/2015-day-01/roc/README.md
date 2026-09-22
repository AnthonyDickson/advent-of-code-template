# Advent of Code - Roc

A [Roc](https://www.roc-lang.org/) template for Advent of Code, built on the
[basic-cli](https://github.com/roc-lang/basic-cli) platform.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#roc` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed. The dev shell provides a pinned nightly build of Roc's new compiler, which is how Roc currently
ships; the version nixpkgs packages is the older alpha4 line.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```

- Run the program:

  ```shell
  just run
  ```

- Build an optimized executable at `./main`, then run it:

  ```shell
  just build
  ./main
  ```

- Type-check the app without running it:

  ```shell
  just check
  ```

- Format the sources:

  ```shell
  just fmt
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

## Layout

- `src/Aoc.roc` holds `solve_part_one` and `solve_part_two`, the two functions to implement, plus the `expect` tests
  that `just test` runs.
- `main.roc` reads `input.txt` and prints both answers.

## Good to know

- Roc keeps compiling after it reports an error, and runs the program anyway when the error is not fatal, so reach for
  `just check` when `just run` prints output despite diagnostics.
- `just test` only compiles `src/Aoc.roc`, so it needs nothing downloaded. The first `just run`, `just check` or `just
  build` fetches the `basic-cli` platform and caches it under `~/.cache/roc`, so that first run needs network.

## Upgrading Roc

Roc has no stable release yet. The compiler version is pinned in two places that have to move together:

- the `roc` entry in the shared [nix/devshells.nix](../../../nix/devshells.nix), and
- the `roc:` entry in the `app` header of `main.roc`.
