namespace Aoc.Parsing

open System

/// Parsers for whitespace. Auto-opened with the namespace, so `open
/// Aoc.Parsing` is enough to use them.
[<AutoOpen>]
module WhitespaceParsers =
    open Parser

    /// Parse a single whitespace character.
    let whitespaceChar =
        let predicate = Char.IsWhiteSpace
        let label = "whitespace"
        satisfy predicate label

    /// Parse zero or more whitespace characters.
    let spaces = many whitespaceChar

    /// Parse one or more whitespace characters.
    let spaces1 = many1 whitespaceChar
