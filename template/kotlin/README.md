# Advent of Code - Kotlin

A Kotlin/JVM template for Advent of Code, built with [Gradle](https://gradle.org/) and its Kotlin DSL.

The solutions are written in a functional style: pure, expression-bodied functions, function references, and collection
pipelines in place of mutable state. Two libraries are on the classpath for when the standard library falls short,
though the starter code does not use them:

- [Arrow](https://arrow-kt.io/) for errors as values: `Either`, the `either { }` builder, and `Raise` for functions that
  can fail.
- [kotlinx.collections.immutable](https://github.com/Kotlin/kotlinx.collections.immutable) for persistent data
  structures such as `PersistentList` and `PersistentMap`, whose `adding`/`putting` return a new collection that shares
  structure with the old one.

See `examples/2015-day-01/kotlin` for both in use. The build treats warnings as errors and enables Kotlin's return value
checker, so discarding the result of a pure function (for example calling `map` and ignoring the list it returns) fails
the build.

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#kotlin` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

Gradle comes from the dev shell, so the project has no Gradle wrapper. It downloads the Kotlin compiler and the test
libraries on the first run and caches them under `~/.gradle`.

## Useful Commands

- Build and run:

  ```shell
  just run
  ```

- Run tests:

  ```shell
  just test
  ```

- Package an executable jar and run it:

  ```shell
  just build
  java -jar build/libs/aoc.jar
  ```

- Format the entire project with `ktfmt`:

  ```shell
  just fmt
  ```

- Benchmark:

  ```shell
  just benchmark
  ```
