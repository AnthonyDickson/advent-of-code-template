# Advent of Code - Swift

A Swift template for Advent of Code.

## Getting Started

Refer to [flake.nix](./flake.nix) for the packages needed to compile this project.
If you have `nix`, you can run `nix develop` to enter a dev shell with all of the dependencies installed.

> [!IMPORTANT]
> Assumes swift 6.2.1 and sourcekit-lsp must be installed manually, currently swift is broken on NixOS.

## Useful Commands

- Build and run:

  ```shell
  make run
  ```

- Run tests:

  ```shell
  make test
  ```

- Benchmark:

  ```shell
  make benchmark
  ```
