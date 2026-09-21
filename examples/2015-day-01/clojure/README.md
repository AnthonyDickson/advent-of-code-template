# Advent of Code - Clojure

A Clojure template for Advent of Code, using the [Clojure CLI](https://clojure.org/guides/deps_and_cli) with a
[`deps.edn`](https://clojure.org/reference/deps_edn) project.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#clojure` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The Clojure CLI downloads Clojure and the test runner on the first run and caches them under `~/.m2` and `~/.gitlibs`.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```

- Run the program:

  ```shell
  just run
  ```

- Package an executable uberjar and run it:

  ```shell
  just build
  java -jar target/aoc.jar
  ```

- Format the project with `cljfmt`, then lint it with `clj-kondo`:

  ```shell
  just fmt
  just lint
  ```

- Benchmark:

  ```shell
  just benchmark
  ```
