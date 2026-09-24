# Results recorder

Benchmarks an Advent of Code solution with its own `just benchmark` recipe and records the numbers, and the application
code's line count, in a `RESULTS.md` table.

```shell
just record 2026-day-05           # from the repository root
uv run aoc-results 2026-day-05    # from this directory
uv run aoc-results --help
```

Run it inside the language's dev shell: `just benchmark` needs that language's toolchain, `hyperfine`, and GNU `time`,
and the line count needs `tokei`.

```shell
nix develop .#rust -c just record 2026-day-05
```

One row is written per day and part:

| Day (Part) | Language                              | Baseline Time | Total Time | Solution Time | Peak RAM (KiB) | Lines |
| :--------- | :------------------------------------ | ------------: | ---------: | ------------: | -------------: | ----: |
| 1 (Both)   | ![Rust](tools/results/icons/rust.svg) |        718 µs |     790 µs |         72 µs |          2,268 |    32 |

`Lines` is the code `tokei` counts in the solution folder with test files, build recipes, and project metadata left out.
Files in a language `tokei` cannot read, such as Shakespeare's `.spl` plays, contribute nothing.

Language cells use a vendored monochrome SVG from [`icons/`](./icons/README.md) where available; Prolog, roc, and
shakespeare show the plain name.

## Flags

| Flag                | Meaning                                                         |
| ------------------- | --------------------------------------------------------------- |
| `--repo PATH`       | Repository root, instead of searching upwards from the folder.  |
| `--file PATH`       | Markdown file to update, instead of `<repo>/RESULTS.md`.        |
| `--language NAME`   | Template the folder was copied from, instead of detecting it.   |
| `--day N`           | Puzzle day, instead of reading it from the folder name.         |
| `--part {1,2,both}` | Which part the row covers. Defaults to `both`.                  |
| `--baseline US`     | Baseline in microseconds, instead of benchmarking the template. |
| `--input PATH`      | Puzzle input, instead of `<folder>/input.txt`.                  |

## Development

```shell
uv run pytest
uv run ruff check
uv run ruff format
```
