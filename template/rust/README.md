# Advent of Code - Rust

An Rust template for Advent of Code.

## Getting Started

Refer to [flake.nix](./flake.nix) for the packages needed to compile this project.
If you have `nix`, you can run `nix develop` to enter a dev shell with all of the dependencies installed.

## Useful Commands

- Build and run:

  ```shell
  cargo run
  ```

- Run tests:

  ```shell
  cargo test
  ```

- Benchmark:

  ```shell
  cargo build --release
  hyperfine -N ./target/release/aoc
  ```
