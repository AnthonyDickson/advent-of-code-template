# AGENTS.md

Guidance for agents working in this repository.

## What this repo is

A collection of self-contained Advent of Code starter projects. There is **no
build at the repo root** and **no CI**. The root `README.md` explains the user
workflow: copy one language folder out of `template/`, drop the puzzle input in
as `input.txt`, and implement the two solution functions.

```
template/<lang>/          starter project, one per language
examples/2015-day-01/<lang>/   reference solutions for Day 1, 2015
```

- `template/` has 10 languages: `c`, `elixir`, `gleam`, `go`, `haskell`,
  `ocaml`, `python`, `rust`, `swift`, `zig`.
- `examples/` has 8 (no `haskell` or `elixir`). Examples are **snapshots** and
  can lag behind the templates; do not assume they are in sync. For example the
  Python example has no `Makefile`, and the Gleam example has a leftover empty
  `.github/workflows/` directory.

Each language folder is an independent project. Always run commands from inside
the specific `template/<lang>` or `examples/<lang>` directory, never the root.

## The shared AoC contract

Every template follows the same shape, adapted to language idiom:

1. A `solve_part_one(input)` and `solve_part_two(input)` function returning an
   integer solution.
2. A CLI entry point that reads `input.txt` (except C, see below) and prints
   part one then part two, one per line.
3. Tests covering both parts with placeholder inputs.

Naming differs by language, follow the local convention:
`SolvePartOne` (Go), `solvePartOne` (Haskell, Swift), `solve_part_one`
(C, Python, Rust, Elixir, Gleam, OCaml, Zig). Filenames follow
`aoc`/`aoc_test` style naming (e.g. `aoc.go`/`aoc_test.go`,
`aoc_test.exs`, `AoCTests.swift`).

Language-specific quirks that are easy to get wrong:

- **OCaml** is the odd one out: `Aoc.load_input` returns a `string list`
  (lines), so `solve_part_one`/`solve_part_two` take `string list`, not
  `string`. The executable is `bin/main.ml` (referenced by the Makefile as
  `_build/default/bin/main.exe`, invoked via `dune exec aoc`).
- **C** takes the input path as `argv[1]` instead of hardcoding `input.txt`,
  and `make run` passes `input.txt` explicitly. It has a hand-rolled test
  harness (`tests/test_aoc.c`) using `TEST`/`RUN_TEST`/`ASSERT_EQ` macros rather
  than a framework.
- **Rust** uses `edition = "2024"`; tests live in an inline `#[cfg(test)] mod
  tests` in `src/main.rs`.
- **Swift** tests use swift-testing (`import Testing`, `@Test`), which is why
  `make test` runs `swift test --disable-xctest`. The `AoC` library target and
  the `@main` struct are both named `AoC`; the executable product is `aoc-cli`.
- **Haskell**'s Makefile declares `fmt` in `.PHONY` but has **no recipe**, so
  `make fmt` is a no-op. Tests use HUnit via a `test-suite` stanza in `aoc.cabal`.
- **Elixir** runs doctests: `test/aoc_test.exs` has `doctest Aoc`, so any
  `@doc` example in `lib/aoc.ex` is executed by `mix test` and must stay correct.
  The CLI is an escript (`main_module: Aoc.CLI`) built by `make build`.
- **Go** builds a binary named `cli` (not `aoc`) to avoid colliding with the
  `aoc/` package directory. Tests are an external `package aoc_test`.
- **Zig** has no `build` target; the release build is hidden as a dependency of
  the `benchmark` target.

## Commands

Run from within a language directory. Not every language defines every target
(for example Python has no `build`/`clean`, Gleam and C have no `fmt`); the
root README's promise of `test`/`run`/`benchmark` holds everywhere.

| Language | test | run | build | fmt | lint |
|---|---|---|---|---|---|
| c | `make test` | `make run` | `make` | - | - |
| elixir | `make test` | `make run` | `make build` | `make fmt` | - |
| gleam | `make test` | `make run` | `make build` | - | - |
| go | `make test` | `make run` | `make build` | `make fmt` | `make lint` |
| haskell | `make test` | `make run` | `make build` | `make fmt` (no-op) | - |
| ocaml | `make test` | `make run` | `make build` | `make fmt` | - |
| python | `make test` | `make run` | - | `make fmt` | - |
| rust | `make test` | `make run` | `make build` | `make fmt` | - |
| swift | `make test` | `make run` | `make build` | `make fmt` | - |
| zig | `make test` | `make run` | - | `make fmt` | - |

Notes:

- Watch mode is used in two places: OCaml `make run` (`dune exec aoc -w`) and
  `make test` (`dune runtest -w`), and Zig `make test` (`zig build --watch
  test`). These commands do not exit on their own.
- `make benchmark` runs `hyperfine` and GNU `time -v` (for peak RAM), so it
  needs both tools plus a release build. Requires the Nix dev shell.
- OCaml has a REPL with project modules loaded: `dune utop`.

## Dev environment (Nix)

Every language folder contains a `flake.nix` and `flake.lock` pinning the
toolchain and dev tools (`gnumake`, `dprint`, `hyperfine`, `time`, plus an LSP).
There is no top-level flake.

```shell
cd template/rust
nix develop -c fish   # or any shell; omit -c to use $SHELL
```

- Swift is the exception: its flake does **not** install Swift or
  sourcekit-lsp (Swift is broken on NixOS). You must have Swift 6.2.1
  (see `.swift-version`) installed manually.
- Benchmark tooling and formatters are only available inside the flake, so
  failures about `hyperfine`/`dprint` usually mean you are not in the shell.

## Formatting and style

- **Markdown** is formatted with `dprint` (configured per folder via
  `dprint.json`, `lineWidth: 120`) and Helix is set up to run `dprint fmt
  --stdin md` (`.helix/languages.toml`, ruler 120). `make fmt` targets format
  *code*, not markdown.
- Language style is enforced implicitly by the toolchains: OCaml uses the
  `janestreet` profile (`.ocamlformat`), Rust `cargo fmt` (edition 2024),
  Haskell `GHC2024` with `-Wall`, Python `ruff`, Elixir `mix format`
  (`.formatter.exs`), Go `go fmt` + `golangci-lint`, Swift `swift format`,
  Zig `zig fmt src/`, C compiled with `-Wall -Wextra -std=c11`.
- Commit history uses Conventional Commits (`feat:`, `chore:`, `refactor:`,
  `fix:`).

## Gotchas

- `**/input.txt` is ignored globally; puzzle inputs are never committed.
- Each language's `.gitignore` covers its own build output (e.g. `target/`,
  `_build/`, `zig-out/`, `.build/`, `cli`, `aoc`, `compile_commands.json`).
  The working tree will often contain ignored build artifacts; do not commit
  them and do not treat their absence as an error.
- C uses `clangd`, which needs `compile_commands.json`. Generate it with
  `bear -- make clean && bear -- make` (see `template/c/README.md`).
- Adding a new language means adding a full `template/<lang>/` folder with
  `Makefile`, `flake.nix`/`flake.lock`, `dprint.json`, `.helix/languages.toml`,
  `README.md`, `.gitignore`, language config, source, and tests.
