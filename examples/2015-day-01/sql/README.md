# Advent of Code - SQL (DuckDB)

A template for Advent of Code written in SQL for [DuckDB](https://duckdb.org/), the in-process analytical database.
There is no procedural code: the two solutions are macros over the puzzle input, and `main.sql` is a short CLI script
that reads `input.txt` and prints both answers.

## Getting Started

Refer to the repository's shared [flake.nix](../../../flake.nix) for the packages needed to run this project. If you
have `nix`, run `nix develop .#sql` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

DuckDB has no package manager and this project has no dependencies, so nothing is fetched: the dev shell and `input.txt`
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

- Parse and bind the solution macros without running them:

  ```shell
  just build
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

`just run` reads `input.txt`, so save the puzzle input first. `just test` and `just build` do not need it.

## Layout

- `src/aoc.sql` holds `solve_part_one` and `solve_part_two`, the two macros to implement.
- `main.sql` reads `input.txt` and prints both answers.
- `tests/test_aoc.sql` holds the example cases that `just test` runs.

## Writing a solution

`read_text('input.txt')` reads the file as a one-row table whose `content` column is the whole puzzle input, trailing
newline and all. From there the usual SQL applies, and DuckDB's list functions are what make it comfortable:

- `string_split(content, chr(10))` gives the lines as a list, and `regexp_extract_all(content, '.')` gives the
  characters; `regexp_extract_all(content, '[0-9]+')` pulls the numbers out.
- `unnest(list) WITH ORDINALITY AS t(value, position)` pairs each element with its 1-based position, which is how a
  puzzle that counts from the start of the input gets its index.
- `list_transform`, `list_filter` and `list_reduce` map over a list without leaving SQL, while `list_sum`, `list_max`
  and friends collapse one.
- Window functions (`sum(x) OVER (ORDER BY position)`) carry a running total down the rows, and a `WITH RECURSIVE` CTE
  is the way to loop when the puzzle does not fit in one pass.

Lambdas changed syntax in DuckDB 1.4: write `list_transform(xs, lambda x: x + 1)`. The older `x -> x + 1` still works
but prints a deprecation warning on every call.

### Getting the answers out

SQL has no `print`, so the answers leave the script as the result sets of two `SELECT`s: one calls `solve_part_one`, the
other `solve_part_two`, and the `run` recipe asks the CLI for one value per line:

```shell
duckdb -batch -bail -no-init -noheader -list < main.sql
```

`.read` is a CLI command rather than SQL, which is why `main.sql` is fed to the CLI on standard input instead of being
named as an argument. The flags are:

- `-list -noheader` prints each row as a plain line, with no box or column header around the answer.
- `-batch` keeps the CLI in non-interactive mode even when a terminal is attached.
- `-bail` stops at the first error and exits non-zero, so a broken solution does not print half an answer.
- `-no-init` skips `~/.duckdbrc`, so a stray setting cannot change how the solution runs.

### Tests

`tests/test_aoc.sql` is a script too: it `.read`s the solution, defines an `assert_example` macro that calls DuckDB's
`error()` on the first case that fails, and runs every case in one query that ends by printing `all N examples passed`.
Because `error()` aborts the run, reaching the summary is what "every example passed" means, and a failure names the
input it was given.

## Notes

- DuckDB has no compiler, so `just build` parses and binds `src/aoc.sql` instead of producing a binary: `CREATE MACRO`
  reports an unknown column or function as soon as the macro is defined.
- `check` is a reserved word in DuckDB and cannot be used as a macro name; `assert_example` in the tests is named around
  that.
- DuckDB runs a query across every core by default, so add `PRAGMA threads=1;` when a benchmark timing looks noisy.
- No SQL formatter is wired into this template, so there is no `just fmt` or `just lint`: the recipes are `test`, `run`,
  `build` and `benchmark`, and the SQL is kept in shape by hand.
