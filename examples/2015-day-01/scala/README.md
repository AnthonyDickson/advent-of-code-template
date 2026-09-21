# Advent of Code - Scala

A Scala 3 template for Advent of Code, built with [Scala CLI](https://scala-cli.virtuslab.org/).

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#scala` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

Scala CLI downloads the Scala compiler and any libraries on the first run and caches them under `~/.cache/scalacli`.

## Useful Commands

- Build and run:

  ```shell
  just run
  ```

- Run tests:

  ```shell
  just test
  ```

- Package an executable assembly and run it:

  ```shell
  just build
  ./aoc
  ```

- Format the entire project with `scalafmt`:

  ```shell
  just fmt
  ```

- Benchmark:

  ```shell
  just benchmark
  ```
