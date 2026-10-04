namespace Aoc.Parsing

/// Infix versions of the combinators, for building parsers in a more
/// expression-oriented style. Auto-opened with the namespace, so `open
/// Aoc.Parsing` is enough to use them.
[<AutoOpen>]
module Operators =
    open Parser

    /// Try the left parser, falling back to the right one.
    let (<|>) = orElse

    /// Infix `bindP`.
    let (>>=) p f = bindP f p

    /// Infix `mapP`, with the function first.
    let (<!>) = mapP

    /// Pipe-friendly `mapP`, with the parser first.
    let (|>>) xP fP = mapP fP xP

    /// Sequence two parsers into a parser of a pair.
    let (.>>.) = andThen

    /// Apply a parser producing a function to a parser producing a value.
    let (<*>) = applyP

    /// Keep the left result only.
    let (.>>) = keepLeft

    /// Keep the right result only.
    let (>>.) = keepRight

    /// Replace a parser's label.
    let (<?>) parser label = setLabel label parser
