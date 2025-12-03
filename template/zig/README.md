# Advent of Code - Zig

An Zig template for Advent of Code.

## Getting Started

Refer to [flake.nix](./flake.nix) for the packages needed to compile this project.
If you have `nix`, you can run `nix develop` to enter a dev shell with all of the dependencies installed.

## Useful Commands


- Build, run and watch for file changes:

  ```shell
  zig build --watch run
  ```

- Run tests and watch for file changes:

  ```shell
  zig build --watch test
  ```

- Benchmark:

  ```shell
  zig build --release=fast
  hyperfine -N ./zig-out/bin/aoc
  ```
