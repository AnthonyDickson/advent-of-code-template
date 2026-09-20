# AGENTS.md

Guidance for agents working in this repository.

## What this repo is

A collection of self-contained Advent of Code starter projects. There is **no build at the repo root** and **no CI**.
The root `README.md` explains the user workflow: copy one language folder out of `template/`, drop the puzzle input in
as `input.txt`, and implement the two solution functions.

```
template/<lang>/          starter project, one per language
examples/2015-day-01/<lang>/   reference solutions for Day 1, 2015
```

- `template/` has 8 languages: `elixir`, `gleam`, `go`, `haskell`, `ocaml`, `python`, `rust`, `zig`.
- `examples/` mirrors `template/` with one example per language. Examples are **snapshots** and can lag behind the
  templates; do not assume they are in sync. For example the Gleam example has a leftover empty `.github/workflows/`
  directory.

Each language folder is an independent project. Always run commands from inside the specific `template/<lang>` or
`examples/<lang>` directory, never the root.

## The shared AoC contract

Every template follows the same shape, adapted to language idiom:

1. A `solve_part_one(input)` and `solve_part_two(input)` function returning an integer solution.
2. A CLI entry point that reads `input.txt` and prints part one then part two, one per line.
3. Tests covering both parts with placeholder inputs.

Naming differs by language, follow the local convention: `SolvePartOne` (Go), `solvePartOne` (Haskell), `solve_part_one`
(Python, Rust, Elixir, Gleam, OCaml, Zig). Filenames follow `aoc`/`aoc_test` style naming (e.g. `aoc.go`/`aoc_test.go`,
`aoc_test.exs`).

Language-specific quirks that are easy to get wrong:

- **OCaml** is the odd one out: `Aoc.load_input` returns a `string list` (lines), so `solve_part_one`/`solve_part_two`
  take `string list`, not `string`. The executable is `bin/main.ml` (referenced by the justfile as
  `_build/default/bin/main.exe`, invoked via `dune exec aoc`).
- **Rust** uses `edition = "2024"`; tests live in an inline `#[cfg(test)] mod tests` in `src/main.rs`.
- **Haskell** is formatted with `ormolu` (installed in the dev shell); tests use `tasty` with `tasty-hunit` via a
  `test-suite` stanza in `aoc.cabal`. `template/haskell/hie.yaml` maps each source directory to its cabal component so
  HLS resolves `Aoc`/`tasty` even when the repository is opened at its root.
- **Elixir** runs doctests: `test/aoc_test.exs` has `doctest Aoc`, so any `@doc` example in `lib/aoc.ex` is executed by
  `mix test` and must stay correct. The CLI is an escript (`main_module: Aoc.CLI`) built by `just build`; a missing
  `input.txt` is reported on stderr with a non-zero exit code.
- **Go** builds a binary named `cli` (not `aoc`) to avoid colliding with the `aoc/` package directory. Tests are an
  external `package aoc_test`.
- **Zig**'s `build` recipe produces a release binary that the `benchmark` recipe depends on.

## Commands

Run from within a language directory. Not every language defines every recipe (for example Python has no
`build`/`clean`); the root README's promise of `test`/`run`/`benchmark` holds everywhere. Every justfile also has a
`default` recipe that prints `just --list`, so running `just` alone shows all recipes.

| Language | test        | run        | build        | fmt        | lint        |
| -------- | ----------- | ---------- | ------------ | ---------- | ----------- |
| elixir   | `just test` | `just run` | `just build` | `just fmt` | -           |
| gleam    | `just test` | `just run` | `just build` | `just fmt` | -           |
| go       | `just test` | `just run` | `just build` | `just fmt` | `just lint` |
| haskell  | `just test` | `just run` | `just build` | `just fmt` | -           |
| ocaml    | `just test` | `just run` | `just build` | `just fmt` | -           |
| python   | `just test` | `just run` | -            | `just fmt` | `just lint` |
| rust     | `just test` | `just run` | `just build` | `just fmt` | `just lint` |
| zig      | `just test` | `just run` | `just build` | `just fmt` | -           |

Notes:

- Watch mode is used in two places: OCaml `just run` (`dune exec aoc -w`) and `just test` (`dune runtest -w`), and Zig
  `just test` (`zig build --watch test`). These commands do not exit on their own.
- `just benchmark` runs `hyperfine` and GNU `time -v` (for peak RAM), so it needs both tools and, where the template
  defines one, the output of `just build`. Requires the Nix dev shell.
- OCaml has a REPL with project modules loaded: `dune utop`.

## Dev environment (Nix)

A single top-level [`flake.nix`](./flake.nix) defines every dev environment; there are no per-language flakes.
Toolchains are pinned to explicit versions in `nix/devshells.nix`, and the shared tools (`just`, `fd`, `dprint`,
`hyperfine`, `time`) are added to every shell.

```shell
nix develop .#rust -c fish   # pick a language; omit -c to use $SHELL
```

- `devShells.default` (plain `nix develop`) contains only the shared tooling.
- Benchmark tooling and formatters are only available inside the flake, so failures about `hyperfine`/`dprint` usually
  mean you are not in the shell.
- Flakes only see git-tracked files, so `git add` new flake files before running `nix develop`.

## Dependency upgrades

Nothing here is updated automatically: there is no CI and no dependency bot. Check and upgrade by hand inside the
relevant dev shell, then re-run `just test`. Lockfiles (`manifest.toml`, `Cargo.lock`, `aoc.opam`) are committed and are
regenerated by the language tool, never edited by hand.

| Language | Check              | Upgrade                                          |
| -------- | ------------------ | ------------------------------------------------ |
| elixir   | `mix hex.outdated` | `just update`                                    |
| gleam    | `just outdated`    | `just update`                                    |
| go       | `just outdated`    | `just update`                                    |
| haskell  | `just outdated`    | edit the bounds in `aoc.cabal`, then `just test` |
| ocaml    | `ocamlfind list`   | see the OCaml note below                         |
| python   | `just outdated`    | widen the bounds in `pyproject.toml`             |
| rust     | `just outdated`    | `just update`                                    |
| zig      | -                  | see the Zig note below                           |

- `just outdated`/`just update` only exist where the language ships a suitable command, so `just --list` is the source
  of truth for a given template.
- Elixir's `mix hex.outdated` needs the Hex archive, which is not installed in the dev shell (`mix local.hex` installs
  it); `just update` (`mix deps.update --all`) works without it.
- Haskell is deliberately pinned to GHC 9.12 because the 9.14 toolchain is broken, so `cabal outdated` reporting a newer
  `base` is expected and must not be acted on. The `tasty` bounds are open-ended lower bounds and already admit the
  newest releases.
- Python declares open lower bounds (`pytest>=8`, `ruff>=0.16`) and ships no lockfile; `just outdated` (`uv pip compile
  --upgrade --group dev`) shows what they currently resolve to, while the dev shell supplies the actual pytest/ruff.
- OCaml and Zig get their packages from the nix dev shell rather than a package manager, so their versions move with
  nixpkgs. Zig has no dependencies today (`build.zig.zon` has an empty `.dependencies`); add one with `zig fetch
  --save`.

### Toolchains and plugins

The remaining pins live at the repository root and are updated from there:

```shell
just update-flake   # move the nixpkgs and rust-overlay pins in flake.lock
just update-dprint  # bump the plugins pinned in dprint.json
```

- `nix flake update` moves every toolchain at once, so verify each language afterwards. OCaml and Zig tests run in watch
  mode and never exit, so prefer `nix develop .#<lang> -c sh -c 'cd template/<lang> && timeout 60 just test'` or run the
  language's `build` recipe instead.
- `nix/devshells.nix` pins explicit version attributes (`go_1_27`, `zig_0_16`, `ghc912`, ...). Re-check it after a flake
  update and bump any attribute that has a newer sibling; tools on unversioned attributes follow nixpkgs automatically.
- `dprint config update` may rewrite a plugin entry as an npm specifier (`npm:@dprint/markdown@0.24.0`) even when the
  version itself is unchanged.

## Formatting and style

- **Markdown** is formatted with `dprint` and hard wrapped at 120 columns. Both formatter configs are shared at the
  repository root: a single `dprint.json` and a single `.helix/languages.toml` that makes Helix run `dprint fmt --stdin
  md` with a 120 column ruler. `just fmt` recipes format _code_, not markdown.
- Language style is enforced implicitly by the toolchains: OCaml uses the `janestreet` profile (`.ocamlformat`), Rust
  `cargo fmt` (edition 2024, `rustfmt.toml` pins `style_edition = "2024"`) plus `cargo clippy`, Haskell `ormolu` with
  `GHC2024` and `-Wall` plus extra warnings, Python `ruff format`/`ruff check`, Elixir `mix format` (`.formatter.exs`),
  Go `go fmt` + `golangci-lint`, Zig `zig fmt src/`.

## Commits and pull requests

- Commit history uses Conventional Commits (`feat:`, `chore:`, `refactor:`, `fix:`); keep the subject line under 72
  characters and describe the outcome for a reader unfamiliar with the change.
- There is no CI, so run `just test` (plus `just fmt`/`just lint` where available) inside the language directory before
  committing.

## Security

- Never commit puzzle inputs or session cookies: `input.txt` is git-ignored and Advent of Code asks that inputs stay
  private. Keep test fixtures synthetic (copied from the puzzle statement), not the real input.
- Solutions only read `input.txt`; there is no network code, and none should be added. Do not embed a personal AoC
  session token in source or config.

## Gotchas

- `**/input.txt` is ignored globally; puzzle inputs are never committed.
- Each language's `.gitignore` covers its own build output (e.g. `target/`, `_build/`, `dist-newstyle/`, `zig-out/`,
  `build`, `cli`, `aoc`, `__pycache__/`). The working tree will often contain ignored build artifacts; do not commit
  them and do not treat their absence as an error.
- Adding a new language means adding a full `template/<lang>/` folder with `justfile`, `README.md`, `.gitignore`,
  language config, source, and tests, plus an entry in `nix/devshells.nix`. Markdown and Helix config are shared at the
  repository root, so no per-language copies are needed.
