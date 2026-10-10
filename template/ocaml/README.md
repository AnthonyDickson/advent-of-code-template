# Advent of Code - OCaml

An OCaml template for Advent of Code.

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#ocaml` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

## Useful Commands

- Interpreter (REPL) with project modules:

  ```shell
  dune utop
  ```

- Build with the release profile:

  ```shell
  just build
  ```

- Build and run, once or watching for file changes:

  ```shell
  just run
  just run-watch
  ```

- Run tests, once or watching for file changes:

  ```shell
  just test
  just test-watch
  ```

- Format the entire project:

  ```shell
  just fmt
  ```

- Compile and run the native binary:

  ```shell
  just benchmark
  ```
