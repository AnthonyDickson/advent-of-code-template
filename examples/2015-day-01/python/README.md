# Advent of Code - Python

A Python template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#python` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides Python and `uv`. `uv` fetches `pytest` and `ruff` from PyPI into `.venv` on the first `just
test`, `just run` or `just build`, so that first command needs network access; every later run is offline.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```
- Run the program:

  ```shell
  just run
  ```

- Lint and format:

  ```shell
  just lint
  just fmt
  ```

- Benchmark the program:

  ```shell
  just benchmark
  ```

- Create `.venv` from `uv.lock` without running anything:

  ```shell
  just build
  ```

- Check for and upgrade dependencies:

  ```shell
  just outdated
  just update
  ```
