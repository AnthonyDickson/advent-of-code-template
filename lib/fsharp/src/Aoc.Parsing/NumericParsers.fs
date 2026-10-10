namespace Aoc.Parsing

open System
open System.Globalization

/// Parsers for numbers. Auto-opened with the namespace, so `open Aoc.Parsing`
/// is enough to use them.
[<AutoOpen>]
module NumericParsers =
    open Parser
    open Operators
    open CharParsers

    /// Parse a single ASCII decimal digit.
    let digitChar =
        let predicate = Char.IsAsciiDigit
        let label = "digit"
        satisfy predicate label

    /// Parse one or more digits and return them as a string.
    let digits = manyChars1 digitChar

    /// Parse an integer, with an optional leading `-`, using `tryParse` to
    /// convert the text. A number that does not fit fails, after consuming its
    /// digits, at the position it starts, rather than throwing.
    let private signedInteger label (tryParse : string -> bool * 'a) =
        let text = opt (pchar '-') .>>. digits

        let inner input =
            let reply = runOnInputState text input

            match reply.Outcome with
            | ParseResult.Success ((sign, digits), remainingInput) ->
                let number = if Option.isSome sign then $"-{digits}" else digits

                match tryParse number with
                | true, value -> {
                    Outcome = ParseResult.Success (value, remainingInput)
                    Consumed = reply.Consumed
                  }
                | false, _ ->
                    ParseReply.hardFail label $"{number} is out of range" (ParserPosition.fromInputState input)
            | ParseResult.Failure (_, error, position) -> {
                Outcome = ParseResult.Failure (label, error, position)
                Consumed = reply.Consumed
              }

        { ParseFn = inner; Label = label }

    /// Parse a 32-bit integer, with an optional leading `-`.
    let pint =
        signedInteger "integer" (fun number ->
            Int32.TryParse (number, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture))

    /// Parse a 64-bit integer, with an optional leading `-`. Puzzle answers and
    /// inputs often outgrow `pint`.
    let pint64 =
        signedInteger "integer" (fun number ->
            Int64.TryParse (number, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture))

    /// Parse a float of the form `digits.digits`, with an optional leading `-`.
    let pfloat =
        let label = "float"

        let resultToFloat (((sign, whole), _point), fraction) =
            let value = float $"{whole}.{fraction}"

            match sign with
            | Some _ -> -value
            | None -> value

        opt (pchar '-') .>>. digits .>>. pchar '.' .>>. digits |> mapP resultToFloat
        <?> label
