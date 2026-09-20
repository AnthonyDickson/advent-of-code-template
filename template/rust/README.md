# Advent of Code - Rust

A Rust template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#rust` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

## Useful Commands

- Build and run:

  ```shell
  just run
  ```

- Run tests:

  ```shell
  just test
  ```

- Lint and format:

  ```shell
  just lint
  just fmt
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

- Check for and upgrade dependencies:

  ```shell
  just outdated
  just update
  ```
