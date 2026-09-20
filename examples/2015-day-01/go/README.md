## Advent of Code - Go

A Go template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../../../flake.nix) for the packages needed to compile this project. If
you have `nix`, run `nix develop .#go` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```
- Run the program:

  ```shell
  just run
  ```

- Benchmark the program:
  ```shell
  just benchmark
  ```

See the [justfile](./justfile) for more commands.
