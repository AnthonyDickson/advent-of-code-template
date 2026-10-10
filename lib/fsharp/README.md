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
- `src/Aoc.Parsing/Parser.fs` - the core types (`ParseResult`, `ParseReply`, `Parser`) and the combinators built on
  `bindP`: `satisfy`, `eof`, `orElse`, `choice`, `andThen`, `sequence`, `many`, `many1`, `opt`, `attempt`, `between`,
  `sepBy`, and friends.
- `src/Aoc.Parsing/Operators.fs` - infix aliases (`<|>`, `.>>.`, `|>>`, ...) for building parsers in an
  expression-oriented style.
- `src/Aoc.Parsing/CharParsers.fs` - `pchar`, `anyOf`, the atomic `pstring`, and the `manyChars` helpers.
- `src/Aoc.Parsing/WhitespaceParsers.fs` - `whitespaceChar`, `spaces`, `spaces1`.
- `src/Aoc.Parsing/NumericParsers.fs` - `digitChar`, `digits`, `pint`, `pint64`, `pfloat`. An integer too large for its
  type is a parse failure at its first digit, not an exception.
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

A parser either succeeds, fails without consuming input, or fails _after_ consuming input. Only a failure that consumed
nothing is backtrackable: `orElse` (`<|>`) tries its second alternative only then, and `many`, `many1`, `sepBy` and
`opt` stop or fall back only then. A failure that consumed input is committed and propagates, so a mid-input syntax
error is reported with its position instead of being silently truncated. Wrap a parser in `attempt` to make a partial
match backtrackable; `pstring` is already atomic, so it needs no `attempt`. `Parser.runReply` exposes the consumption
flag alongside the result, and `eof` fails when input remains.

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
