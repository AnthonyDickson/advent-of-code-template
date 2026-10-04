# Advent of Code - F# parser combinators

A small parser combinator library for parsing puzzle input. It lives in `lib/` rather than inside a template or an
example, so the templates stay minimal and the same library can be reused, and ported to other languages, without
dragging a solution along with it.

The combinators are adapted from
[Understanding Parser Combinators](https://fsharpforfunandprofit.com/posts/understanding-parser-combinators).

## Getting Started

The dev shell is the shared `.#fsharp` shell:

```shell
nix develop .#fsharp
```

It pins the SDK, restores `fantomas` and `fsautocomplete` from `.config/dotnet-tools.json`, and exports `DOTNET_ROOT`.

## Layout

- `src/Aoc.Parsing/Position.fs` - `Position`, `InputState`, and `ParserPosition`. The input is split into lines up front
  and the end of a line is reported as a `'\n'`, so a grammar does not have to special-case line breaks.
- `src/Aoc.Parsing/Parser.fs` - the core types (`ParseResult`, `Parser`) and the combinators built on `bindP`:
  `satisfy`, `orElse`, `choice`, `andThen`, `sequence`, `many`, `many1`, `opt`, `between`, `sepBy`, and friends.
- `src/Aoc.Parsing/Operators.fs` - infix aliases (`<|>`, `.>>.`, `|>>`, ...) for building parsers in an
  expression-oriented style.
- `src/Aoc.Parsing/CharParsers.fs` - `pchar`, `anyOf`, `pstring`, and the `manyChars` helpers.
- `src/Aoc.Parsing/WhitespaceParsers.fs` - `whitespaceChar`, `spaces`, `spaces1`.
- `src/Aoc.Parsing/NumericParsers.fs` - `digitChar`, `digits`, `pint`, `pfloat`.
- `tests/Aoc.Parsing.Tests/` - the Expecto tests, one file per module above.

The parser modules are `[<AutoOpen>]`, so a single `open Aoc.Parsing` brings the primitives, the operators, and every
parser into scope. The files stay separate for navigation and for porting; the qualified names (`Parser.run`,
`CharParsers.pchar`) still work when a name is ambiguous.

## Usage

```fsharp
open Aoc.Parsing

let game = pstring "Game " >>. pint .>> pchar ':'
let result = Parser.run game "Game 1: 1 red"
```

`Parser.run` returns a `ParseResult` that is either `Success` or `Failure`. On failure, `ParseResult.toDisplayString`
renders the line and column with a caret under the offending character.

## Useful Commands

- Run the tests:

  ```shell
  just test
  ```

- Build the library:

  ```shell
  just build
  ```

- Format with `fantomas`:

  ```shell
  just fmt
  ```

- Check for and upgrade dependencies:

  ```shell
  just outdated
  just update
  ```
