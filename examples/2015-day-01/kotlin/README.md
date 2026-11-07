# Advent of Code - Kotlin

A Kotlin/JVM template for Advent of Code, built with [Gradle](https://gradle.org/) and its Kotlin DSL.

The solutions are written in a functional style: pure, expression-bodied functions, function references, and collection
pipelines in place of mutable state. Two libraries fill the gaps in the standard library:

- [Arrow](https://arrow-kt.io/) for errors as values. Each solution returns `Either<AocError, Long>`, built with the
  `either { }` builder, and helpers that can fail take a `Raise<AocError>` receiver so they `raise` an error instead of
  throwing one.
- [kotlinx.collections.immutable](https://github.com/Kotlin/kotlinx.collections.immutable) for persistent data
  structures. A `PersistentList` is never changed in place: `adding` returns a new list that shares structure with the
  old one.

The build treats warnings as errors and enables Kotlin's return value checker, so discarding the result of a pure
function (for example calling `adding` on a persistent list and ignoring the list it returns) fails the build.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#kotlin` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

Gradle comes from the dev shell, so the project has no Gradle wrapper. It downloads the Kotlin compiler and the
libraries on the first run and caches them under `~/.gradle`.

The language server is JetBrains' [`kotlin-lsp`](https://github.com/Kotlin/kotlin-lsp), which the repository's Helix
config starts with `kotlin-lsp --stdio`.

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
