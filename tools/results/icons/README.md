# Language icons

One monochrome SVG per language template, linked from the Language column of `RESULTS.md`. They render for every reader
because GitHub serves repository images itself; icon _fonts_ cannot be used, since GitHub strips the stylesheets they
need.

| Source                                  | Licence | Files                          |
| --------------------------------------- | ------- | ------------------------------ |
| [Simple Icons](https://simpleicons.org) | CC0 1.0 | everything except `duckdb.svg` |

Files were fetched from `https://cdn.simpleicons.org/<slug>/8b949e`, where `8b949e` pins them to the one mid grey that
stays legible on GitHub's light and dark themes. Regenerate one with the same URL and slug:

| File          | Slug         | File      | Slug      | File         | Slug         |
| ------------- | ------------ | --------- | --------- | ------------ | ------------ |
| `clojure`     | `clojure`    | `fsharp`  | `fsharp`  | `rust`       | `rust`       |
| `common-lisp` | `commonlisp` | `gleam`   | `gleam`   | `scala`      | `scala`      |
| `elixir`      | `elixir`     | `go`      | `go`      | `typescript` | `typescript` |
| `haskell`     | `haskell`    | `nushell` | `nushell` | `typst`      | `typst`      |
| `ocaml`       | `ocaml`      | `odin`    | `odin`    | `zig`        | `zig`        |
| `python`      | `python`     | `duckdb`  | `duckdb`  |              |              |

`duckdb.svg` stands in for the `sql` template, whose solutions are DuckDB macros rather than a generic SQL dialect, so
`LANGUAGE_ICONS` maps `sql` to it.

Prolog, roc and shakespeare have no icon in Simple Icons or Devicon, so those rows show the plain language name.
