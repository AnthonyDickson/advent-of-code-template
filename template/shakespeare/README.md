# Advent of Code - Shakespeare

A template for Advent of Code written in the
[Shakespeare Programming Language](https://en.wikipedia.org/wiki/Shakespeare_Programming_Language) (SPL), run with the
[`shakespearelang`](https://shakespearelang.com/) interpreter.

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to run this project. If you have
`nix`, run `nix develop .#shakespeare` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell provides Python and `uv`. `uv` fetches the interpreter and its dependencies from PyPI into `.venv` on the
first `just test`, `just run` or `just build`, so that first command needs network access; every later run is offline.

## Useful Commands

- Run tests:

  ```shell
  just test
  ```

- Run the program:

  ```shell
  just run
  ```

- Run one play by hand, with the interpreter's console and debugger alongside it:

  ```shell
  uv run shakespeare run src/part_one.spl < input.txt
  uv run shakespeare debug src/part_one.spl
  uv run shakespeare
  ```

- Fetch the interpreter into `.venv` without running anything:

  ```shell
  just build
  ```

- Lint and format the Python harness:

  ```shell
  just lint
  just fmt
  ```

- Benchmark:

  ```shell
  just benchmark
  ```

## Layout

- `src/part_one.spl` and `src/part_two.spl` are the two plays to implement.
- `aoc.py` is the harness: it feeds `input.txt` to each play and prints the two answers, one per line.
- `tests/test_aoc.py` holds the pytest tests that `just test` runs.

## Writing a solution

SPL has no functions. A play declares a cast, each character of which is an integer variable, and the characters talk to
one another. Exactly two may be on stage at a time, so each line is spoken by one of them and addresses the other:
"you", "thou" and "thee" name whoever is _not_ speaking, and "yourself" is their value. A character's value can also be
read from anywhere by naming it, even from off stage.

Input and output are how a play sees the puzzle:

| Sentence                | Meaning                                          |
| ----------------------- | ------------------------------------------------ |
| `Open your mind!`       | read one character, as its code, into the other  |
| `Listen to your heart!` | read one number into the other                   |
| `Open your heart!`      | print the other character's value as a number    |
| `Speak your mind!`      | print the other character's value as a character |

`Open your mind!` returns -1 once the input runs out, so a play walks the whole puzzle the same way every time:

```
Romeo:
 Open your mind!

Romeo:
 Is Juliet worse than nothing?

Juliet:
 If so, let us proceed to scene III.

Juliet:
 Let us return to scene II.
```

Two details matter when writing a play:

- Characters must be named after a fixed list of Shakespearean characters (`Romeo`, `Juliet`, `Hamlet`, `Othello`,
  `Macbeth`, ...). A name from outside the list is a parse error.
- Part one and part two are separate plays, because a play reads its input once, as a stream. Part two cannot rewind, so
  `aoc.py` gives it a fresh run with its own copy of `input.txt`; put shared helpers in both plays instead.

SPL has no formatter, so `just fmt` and `just lint` only cover `aoc.py` and the tests.
