# Advent of Code - OCaml

An OCaml template for Advent of Code.

## Getting Started

Refer to [flake.nix](./flake.nix) for the packages needed to compile this project.
If you have `nix`, you can run `nix develop` to enter a dev shell with all of the dependencies installed.

## Useful Commands

- Interpreter (REPL) with project modules:

  ```shell
  dune utop
  ```

- Build and watch for file changes:

  ```shell
  dune build -w
  ```

- Build, run and watch for file changes:

  ```shell
  dune exec aoc -w
  ```

- Run tests and watch for file changes:

  ```shell
  dune runtest -w
  ```

- Format the entire project:

  ```shell
  dune build @fmt --auto-promote
  ```
- Compile and run the native binary:

  ```shell
  dune build
  ./_build/default/bin/main.exe
  ```
