# Language lottery

A weighted lottery that picks a language for the day's Advent of Code puzzle, then offers to copy that language's
template into a fresh solution folder and tells you what is left to do.

```shell
just lottery                      # from the repository root
uv run aoc-lottery                # from this directory
uv run aoc-lottery --plain --day 5
```

The tool needs `uv`, which every dev shell in this repository provides. `uv` installs `textual` and the rest of the
dependencies on the first run.

## The TUI

1. **Spin** draws a language. Every template is on the wheel and the table shows each language's weight and chance of
   winning; the draw is weighted, so raising a weight in [`lottery.toml`](../../lottery.toml) makes that language come
   up more often.
1. **Result** does not force the pick: press <kbd>r</kbd> to re-roll as many times as you like, or <kbd>b</kbd> to
   bootstrap the drawn language.
1. **Bootstrap** asks for the year and day (the day is required, the year defaults to the current one). The destination
   defaults to `<year>-day-<dd>` in the repository root and follows the day until you edit it by hand.
1. **Next steps** copies the template, skipping build output and any `input.txt`, and lists everything that is left:
   which file to edit, which functions to implement, and which `just` recipes to run.

Solutions are written to the repository root so that a private repository created from this one has one
`<year>-day-<dd>/` folder per day, next to `template/`. The language that was drawn is not part of the path; add it by
hand in the destination field if a day needs more than one version.

Useful keys: <kbd>s</kbd> spin, <kbd>r</kbd> re-roll, <kbd>b</kbd> bootstrap, <kbd>n</kbd> new draw, <kbd>q</kbd> quit.
The next steps view also scrolls with the arrow keys, <kbd>j</kbd>/<kbd>k</kbd>/<kbd>h</kbd>/<kbd>l</kbd>, and
<kbd>g</kbd>/<kbd>G</kbd> for the top and bottom; those keys are not listed in the footer, which only shows the screen's
own commands.

## Weights

Weights live in the repository root as [`lottery.toml`](../../lottery.toml):

```toml
[weights]
rust = 3    # three times as likely as an untouched language
python = 1
zig = 0     # takes zig off the wheel
```

Every template language defaults to a weight of `1`, and naming a language that has no template is an error. Point the
tool at another file with `--config path/to/weights.toml`.

## Flags

| Flag            | Meaning                                                                   |
| --------------- | ------------------------------------------------------------------------- |
| `--repo PATH`   | Repository root, instead of searching upwards from the current directory. |
| `--config PATH` | Weights file, instead of `<repo>/lottery.toml`.                           |
| `--seed N`      | Seed the draw, for a repeatable result.                                   |
| `--shell NAME`  | Shell used by the printed `nix develop -c` command, instead of `$SHELL`.  |
| `--plain`       | Draw without the TUI: prints the language and can bootstrap one day.      |
| `--day N`       | Day to bootstrap in `--plain` mode.                                       |
| `--year N`      | Year to bootstrap in `--plain` mode, instead of the current year.         |
| `--dest PATH`   | Destination folder for `--plain` mode.                                    |

`--dest` takes a path relative to the repository root or an absolute path. An existing destination is never overwritten.

The plain mode keeps stdout to the drawn language name, so `language=$(uv run aoc-lottery --plain)` stays scriptable,
and prints everything else on stderr.

## Development

```shell
uv run pytest          # tests, including the TUI driven headlessly
uv run ruff check
uv run ruff format
```
