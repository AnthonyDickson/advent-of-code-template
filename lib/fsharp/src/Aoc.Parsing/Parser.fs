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
        | Success(value, _input) -> $"{value}"
        | Failure(label, error, position) ->
            let errorLine = position.CurrentLine |> Option.defaultValue ""
            let colPos = position.Column
            let linePos = position.Line
            let failureCaretPadding = "".PadLeft colPos
            let failureCaret = $"{failureCaretPadding}^{error}"
            $"Line:{linePos} Col:{colPos} Error parsing {label}\n{errorLine}\n{failureCaret}"

/// Whether a parser attempt advanced the input before finishing.
///
/// `Consumed` means the parser changed the input state before it failed, so a
/// surrounding combinator must not backtrack. `NotConsumed` means it failed
/// without touching the input, so an alternative may be tried from the same
/// position. This is Parsec's `Consumed`/`Empty` distinction.
type Consumed =
    | Consumed
    | NotConsumed

/// A parse outcome tagged with whether input was consumed before it finished.
type ParseReply<'a> = {
    Outcome: ParseResult<'a * InputState>
    Consumed: Consumed
}

/// Constructors for `ParseReply`, so the combinators name the branch they take
/// instead of threading record syntax.
module ParseReply =
    /// A success that consumed no input.
    let ok state value = {
        Outcome = Success(value, state)
        Consumed = NotConsumed
    }

    /// A success that consumed input.
    let okConsumed state value = {
        Outcome = Success(value, state)
        Consumed = Consumed
    }

    /// A failure that consumed no input, so the caller may backtrack.
    let softFail label error pos = {
        Outcome = Failure(label, error, pos)
        Consumed = NotConsumed
    }

    /// A failure that consumed input, so the caller must not backtrack.
    let hardFail label error pos = {
        Outcome = Failure(label, error, pos)
        Consumed = Consumed
    }

    /// Combine the consumption of two replies.
    let orConsumed a b =
        if a = Consumed || b = Consumed then
            Consumed
        else
            NotConsumed

/// A parser is a function from an input state to a reply, tagged with a label
/// used when reporting failures.
///
/// Keeping the label beside the function (rather than inside it) is what lets
/// `setLabel` and the `<?>` operator relabel a parser without reimplementing
/// it.
type Parser<'a> = {
    ParseFn: (InputState -> ParseReply<'a>)
    Label: ParserLabel
}

/// The core combinators. Auto-opened with the namespace, so `open Aoc.Parsing`
/// is enough to use `satisfy`, `many`, `between`, and the rest unqualified.
[<AutoOpen>]
module Parser =
    /// Run a parser against an input state.
    let runOnInputState parser input = parser.ParseFn input

    /// Run a parser against a string, returning the full reply. Use this when
    /// the consumption flag matters.
    let runReply parser input =
        runOnInputState parser (InputState.fromString input)

    /// Run a parser against a string, returning only the `ParseResult`.
    let run parser input = (runReply parser input).Outcome

    /// Replace a parser's label. Failures are reported with the new label; the
    /// original error text, position and consumption are preserved.
    let setLabel newLabel parser =
        let inner input =
            match parser.ParseFn input with
            | {
                  Outcome = Failure(_, error, position)
              } as reply -> {
                reply with
                    Outcome = Failure(newLabel, error, position)
              }
            | reply -> reply

        { ParseFn = inner; Label = newLabel }

    /// The parser's current label.
    let getLabel parser = parser.Label

    /// Parse a single character that satisfies a predicate.
    ///
    /// A rejected character does not consume input, so the character is left in
    /// the stream and an alternative or a repetition can still backtrack.
    let satisfy predicate label =
        let inner input =
            let remainingInput, charOpt = InputState.nextChar input

            match charOpt with
            | None -> ParseReply.softFail label "No more input" (ParserPosition.fromInputState input)
            | Some first ->
                if predicate first then
                    ParseReply.okConsumed remainingInput first
                else
                    ParseReply.softFail label $"Unexpected '{first}'" (ParserPosition.fromInputState input)

        { ParseFn = inner; Label = label }

    /// Succeed only at the end of the input, leaving the input untouched.
    ///
    /// When input remains the parser fails without consuming, so a caller can
    /// report trailing junk rather than backtracking into it.
    let eof =
        let label = "end of input"

        let inner input =
            match InputState.nextChar input with
            | _, None -> ParseReply.ok input ()
            | _, Some _ -> ParseReply.softFail label "Expected end of input" (ParserPosition.fromInputState input)

        { ParseFn = inner; Label = label }

    /// Try the first parser, falling back to the second if it fails *without*
    /// consuming input.
    ///
    /// A failure that consumed input is committed: it propagates and the second
    /// parser is never tried. A failure reports the combined label, so a top
    /// level error names every alternative that was tried.
    let orElse parser1 parser2 =
        let label = $"{parser1.Label} orElse {parser2.Label}"

        let inner input =
            match runOnInputState parser1 input with
            | {
                  Outcome = Failure _
                  Consumed = Consumed
              } as committed -> committed
            | { Outcome = Failure _ } ->
                match runOnInputState parser2 input with
                | {
                      Outcome = Failure(_, error, position)
                  } as failed -> {
                    failed with
                        Outcome = Failure(label, error, position)
                  }
                | success -> success
            | success -> success

        { ParseFn = inner; Label = label }

    /// Try each parser in turn, returning the first success.
    let choice parsers = List.reduce orElse parsers

    /// Run `p`, then use its value to choose the next parser. This is the
    /// monadic bind: it builds a parser from each value, so the fixed-shape
    /// combinators (`mapP`, `andThen`, `applyP`) are written without it.
    ///
    /// The combined reply is consumed if either half consumed input.
    let bindP f p =
        let inner input =
            match runOnInputState p input with
            | {
                  Outcome = Failure(label, error, position)
                  Consumed = consumed
              } -> {
                Outcome = Failure(label, error, position)
                Consumed = consumed
              }
            | {
                  Outcome = Success(value, remainingInput)
                  Consumed = consumed
              } ->
                let reply = runOnInputState (f value) remainingInput

                {
                    reply with
                        Consumed = ParseReply.orConsumed consumed reply.Consumed
                }

        let label = $"bind {p.Label}"

        { ParseFn = inner; Label = label }

    /// A parser that succeeds with `x` without consuming any input.
    let returnP x =
        let inner input = ParseReply.ok input x
        let label = "returnP"

        { ParseFn = inner; Label = label }

    /// Apply a function to the value produced by a parser.
    ///
    /// Written directly rather than as `bindP (f >> returnP)`, so a parse does
    /// not build a new parser (and format its label) for every value.
    let mapP f parser =
        let inner input =
            let reply = runOnInputState parser input

            match reply.Outcome with
            | Success(value, remainingInput) -> {
                Outcome = Success(f value, remainingInput)
                Consumed = reply.Consumed
              }
            | Failure(label, error, position) -> {
                Outcome = Failure(label, error, position)
                Consumed = reply.Consumed
              }

        {
            ParseFn = inner
            Label = parser.Label
        }

    /// Run `parser1` then `parser2` and combine their values with `combine`.
    /// A failure keeps the failing parser's label, and the reply is consumed if
    /// either parser consumed input. This is `bindP` specialised to a second
    /// parser that is known up front, so nothing is built during a parse.
    let private combineP combine parser1 parser2 input =
        let first = runOnInputState parser1 input

        match first.Outcome with
        | Failure(label, error, position) -> {
            Outcome = Failure(label, error, position)
            Consumed = first.Consumed
          }
        | Success(value1, remainingInput) ->
            let second = runOnInputState parser2 remainingInput
            let consumed = ParseReply.orConsumed first.Consumed second.Consumed

            match second.Outcome with
            | Failure(label, error, position) -> {
                Outcome = Failure(label, error, position)
                Consumed = consumed
              }
            | Success(value2, remainingInput) -> {
                Outcome = Success(combine value1 value2, remainingInput)
                Consumed = consumed
              }

    /// Run two parsers in sequence, producing a parser of a pair.
    let andThen parser1 parser2 =
        let label = $"{parser1.Label} andThen {parser2.Label}"

        {
            ParseFn = combineP (fun result1 result2 -> result1, result2) parser1 parser2
            Label = label
        }
        |> setLabel label

    /// Apply a parser producing a function to a parser producing a value.
    let applyP fP xP = {
        ParseFn = combineP (fun f x -> f x) fP xP
        Label = $"{fP.Label} applyP {xP.Label}"
    }

    /// Lift a two parameter function into the parser world.
    let lift2 f xP yP = applyP (applyP (returnP f) xP) yP

    /// Turn a list of parsers into a parser of a list.
    let rec sequence parsers =
        let cons head tail = head :: tail
        let consP = lift2 cons

        match parsers with
        | [] -> returnP []
        | head :: tail -> consP head (sequence tail)

    /// Match zero or more occurrences of a parser.
    ///
    /// The repetition stops, and succeeds with what it has collected, only when
    /// the element fails without consuming input. An element that fails *after*
    /// consuming input is committed, so the whole repetition fails with that
    /// error instead of silently returning a partial list.
    let many parser =
        let rec loop state values =
            match runOnInputState parser state with
            | {
                  Outcome = Failure(label, error, position)
                  Consumed = Consumed
              } -> ParseReply.hardFail label error position
            | { Outcome = Failure _ } ->
                let consumed = if List.isEmpty values then NotConsumed else Consumed

                {
                    Outcome = Success(List.rev values, state)
                    Consumed = consumed
                }
            | {
                  Outcome = Success _
                  Consumed = NotConsumed
              } -> failwith $"many applied to a parser that accepts empty input: {parser.Label}"
            | { Outcome = Success(value, next) } -> loop next (value :: values)

        let inner input = loop input []

        let label = $"many {parser.Label}"
        { ParseFn = inner; Label = label }

    /// Match one or more occurrences of a parser.
    let many1 parser =
        let join (first, rest) = first :: rest

        andThen parser (many parser) |> mapP join |> setLabel $"many1 {parser.Label}"

    /// Match zero or one occurrence of a parser.
    ///
    /// A failure that consumed input is committed and propagates, rather than
    /// quietly becoming `None`.
    let opt p = orElse (mapP Some p) (returnP None)

    /// Downgrade a committed failure to a non-consuming one, so an alternative
    /// can run against the original input. This is Parsec's `try`.
    let attempt parser =
        let inner input =
            match runOnInputState parser input with
            | {
                  Outcome = Failure _
                  Consumed = Consumed
              } as reply -> { reply with Consumed = NotConsumed }
            | reply -> reply

        {
            ParseFn = inner
            Label = parser.Label
        }

    /// Alias for `attempt`.
    let tryP = attempt

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
