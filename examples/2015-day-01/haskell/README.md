# Advent of Code - Haskell

A Haskell template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#haskell` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

`hie.yaml` maps each source directory to its cabal component, so HLS resolves `Aoc`, the executable, and `tasty` even
when the repository is opened at its root rather than in this folder.

## Useful Commands

- Build and run:

  ```shell
  just run
  ```

- Run tests:

  ```shell
  just test
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

- Format the entire project:

  ```shell
  just fmt
  ```

- Check for outdated dependencies:

  ```shell
  just outdated
  ```
