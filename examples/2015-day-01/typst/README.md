# Advent of Code - Typst

A template for Advent of Code written in [Typst](https://typst.app/), the typesetting language. A Typst program is a
document, so `main.typ` is the entry point: it reads `input.txt`, renders both answers, and publishes them as metadata
for the CLI to print.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to render this project. If you
have `nix`, run `nix develop .#typst` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

Typst has no package manager and this project has no dependencies, so nothing is fetched: the dev shell and `input.txt`
are all it needs.

## Useful Commands

- Check both solutions against the examples from the puzzle statement:

  ```shell
  just test
  ```

- Print both answers, one per line:

  ```shell
  just run
  ```

- Render `main.typ` to `main.pdf`:

  ```shell
  just build
  ```

- Format and lint the Typst source:

  ```shell
  just fmt
  just lint
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

- Render on every save, for a live preview:

  ```shell
  typst watch main.typ
  ```

Anything that compiles `main.typ` (`just run`, `just build`, `just lint`, `just benchmark` and `typst watch`) reads
`input.txt` while it does so, and therefore needs the puzzle input to be saved first. `just test` checks the examples
and `just fmt` only rewrites source, so neither of those does.

## Layout

- `main.typ` reads `input.txt`, shows both answers, and publishes them as metadata.
- `src/aoc.typ` holds `solve-part-one` and `solve-part-two`, the two functions to implement.
- `tests/test_aoc.typ` holds the example cases that `just test` runs.

## Writing a solution

`read("input.txt")` gives the whole puzzle input as one string. There are no line, word or number helpers to go with it:
`s.split("\n")` gives an array of lines, and `s.clusters()` gives an array of one-character strings, which is what
character-by-character puzzles want. Arrays carry `map`, `filter`, `fold`, `enumerate`, `sum` and `sorted`, and `for`,
`while` and `if`/`else` all work as expressions.

Two limits surprise people, because neither looks like anything special:

- A `while` loop stops after 10,000 iterations with `loop seems to be infinite`. `for` loops are not limited, so drive
  long runs with those or with `range`.
- Function calls nest at most 80 deep, ending in `maximum function call depth exceeded`. A recursive walk over a large
  input has to become a `while` loop with an explicit stack.

### Getting the answers out

Typst cannot print: the only output a program has is the document it renders. The two answers therefore leave `main.typ`
as `#metadata(...)` elements, which `typst eval` reads back out:

```typst
#metadata(part-one) <part-one>
```

```shell
typst eval --in main.typ 'query(<part-one>).first().value'
```

`query` finds the labelled element, `first` unwraps the single match, and `value` is the payload. Keeping the answers in
variables (`#let part-one = solve-part-one(input)`) lets the document show them and publish them at the same time. The
`run` recipe queries the two answers separately, which is what puts them on two lines.
