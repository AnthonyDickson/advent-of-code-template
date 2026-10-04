namespace Aoc.Parsing

/// A short description of what a parser was trying to match, used in error
/// messages (for example `'a'` or `integer`).
type ParserLabel = string

/// A description of why a parser failed at the current position.
type ParserError = string

/// The outcome of running a parser: either the parsed value, or a labelled
/// failure with the position at which parsing stopped.
///
/// A success carries the value *and* the remaining input, so a parser is a
/// function from input state to a new input state. See `Parser`.
type ParseResult<'a> =
    | Success of 'a
    | Failure of ParserLabel * ParserError * ParserPosition

module ParseResult =
    /// Render a result as a human readable message, with a caret under the
    /// column where a failure occurred.
    let toDisplayString result =
        match result with
        | Success (value, _input) -> $"{value}"
        | Failure (label, error, position) ->
            let errorLine = position.CurrentLine |> Option.defaultValue ""
            let colPos = position.Column
            let linePos = position.Line
            let failureCaretPadding = "".PadLeft colPos
            let failureCaret = $"{failureCaretPadding}^{error}"
            $"Line:{linePos} Col:{colPos} Error parsing {label}\n{errorLine}\n{failureCaret}"

/// A parser is a function from an input state to a result, tagged with a label
/// used when reporting failures.
///
/// Keeping the label beside the function (rather than inside it) is what lets
/// `setLabel` and the `<?>` operator relabel a parser without reimplementing
/// it.
type Parser<'a> = {
    ParseFn : (InputState -> ParseResult<'a * InputState>)
    Label : ParserLabel
}

/// The core combinators. Auto-opened with the namespace, so `open Aoc.Parsing`
/// is enough to use `satisfy`, `many`, `between`, and the rest unqualified.
[<AutoOpen>]
module Parser =
    /// Run a parser against an input state.
    let runOnInputState parser input = parser.ParseFn input

    /// Run a parser against a string.
    let run parser input =
        runOnInputState parser (InputState.fromString input)

    /// Replace a parser's label. Failures are reported with the new label; the
    /// original error text and position are preserved.
    let setLabel newLabel parser =
        let inner input =
            match parser.ParseFn input with
            | Success value -> Success value
            | Failure (_, error, position) -> Failure (newLabel, error, position)

        { ParseFn = inner; Label = newLabel }

    /// The parser's current label.
    let getLabel parser = parser.Label

    /// Parse a single character that satisfies a predicate.
    let satisfy predicate label =
        let inner input =
            let remainingInput, charOpt = InputState.nextChar input

            match charOpt with
            | None ->
                let err = "No more input"
                let pos = ParserPosition.fromInputState input
                Failure (label, err, pos)
            | Some first ->
                if predicate first then
                    Success (first, remainingInput)
                else
                    let err = $"Unexpected '{first}'"
                    let pos = ParserPosition.fromInputState input
                    Failure (label, err, pos)

        { ParseFn = inner; Label = label }

    /// Try the first parser, falling back to the second if it fails. A failure
    /// reports the combined label, so a top level error names every alternative
    /// that was tried rather than only the last one.
    let orElse parser1 parser2 =
        let label = $"{parser1.Label} orElse {parser2.Label}"

        let inner input =
            match runOnInputState parser1 input with
            | Success success -> Success success
            | Failure _ ->
                match runOnInputState parser2 input with
                | Success success -> Success success
                | Failure (_, error, position) -> Failure (label, error, position)

        { ParseFn = inner; Label = label }

    /// Try each parser in turn, returning the first success.
    let choice parsers = List.reduce orElse parsers

    /// Run `p`, then use its value to choose the next parser. This is the
    /// monadic bind that every other combinator is built from.
    let bindP f p =
        let inner input =
            match runOnInputState p input with
            | Failure (label, error, pos) -> Failure (label, error, pos)
            | Success (value, remainingInput) ->
                let p2 = f value
                runOnInputState p2 remainingInput

        let label = $"bind {p.Label}"

        { ParseFn = inner; Label = label }

    /// A parser that succeeds with `x` without consuming any input.
    let returnP x =
        let inner input = Success (x, input)
        let label = "returnP"

        { ParseFn = inner; Label = label }

    /// Apply a function to the value produced by a parser.
    let mapP f = bindP (f >> returnP)

    /// Run two parsers in sequence, producing a parser of a pair.
    let andThen parser1 parser2 =
        bindP (fun result1 -> bindP (fun result2 -> returnP (result1, result2)) parser2) parser1
        |> setLabel $"{parser1.Label} andThen {parser2.Label}"

    /// Apply a parser producing a function to a parser producing a value.
    let applyP fP xP =
        bindP (fun f -> bindP (fun x -> returnP (f x)) xP) fP

    /// Lift a two parameter function into the parser world.
    let lift2 f xP yP = applyP (applyP (returnP f) xP) yP

    /// Turn a list of parsers into a parser of a list.
    let rec sequence parsers =
        let cons head tail = head :: tail
        let consP = lift2 cons

        match parsers with
        | [] -> returnP []
        | head :: tail -> consP head (sequence tail)

    /// Consume zero or more occurrences of `parser`. Always succeeds, so it
    /// never has to report a failure.
    let rec private parseZeroOrMore parser input =
        let rec loop remainingInput values =
            match runOnInputState parser remainingInput with
            | Failure _ -> List.rev values, remainingInput
            | Success (value, remainingInput) -> loop remainingInput (value :: values)

        loop input []

    /// Match zero or more occurrences of a parser.
    let many parser =
        let inner input = Success (parseZeroOrMore parser input)
        let label = $"many {parser.Label}"
        { ParseFn = inner; Label = label }

    /// Match one or more occurrences of a parser.
    let many1 parser =
        let join (first, rest) = first :: rest

        andThen parser (many parser) |> mapP join |> setLabel $"many1 {parser.Label}"

    /// Match zero or one occurrence of a parser.
    let opt p = orElse (mapP Some p) (returnP None)

    /// Keep the result of the left parser only.
    let keepLeft p1 p2 =
        andThen p1 p2 |> mapP (fun (left, _) -> left)

    /// Keep the result of the right parser only.
    let keepRight p1 p2 =
        andThen p1 p2 |> mapP (fun (_, right) -> right)

    /// Match `p2` between the separators `p1` and `p3`.
    let between p1 p2 p3 = keepLeft (keepRight p1 p2) p3

    /// One or more occurrences of `p` separated by `sep`.
    let sepBy1 p sep =
        let join (first, rest) = first :: rest
        andThen p (many (keepRight sep p)) |> mapP join

    /// Zero or more occurrences of `p` separated by `sep`.
    let sepBy p sep = orElse (sepBy1 p sep) (returnP [])
