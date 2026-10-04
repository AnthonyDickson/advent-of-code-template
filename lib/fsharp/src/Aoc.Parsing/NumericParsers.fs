namespace Aoc.Parsing

open System

/// Parsers for numbers. Auto-opened with the namespace, so `open Aoc.Parsing`
/// is enough to use them.
[<AutoOpen>]
module NumericParsers =
    open Parser
    open Operators
    open CharParsers

    /// Parse a single decimal digit.
    let digitChar =
        let predicate = Char.IsDigit
        let label = "digit"
        satisfy predicate label

    /// Parse one or more digits and return them as a string.
    let digits = manyChars1 digitChar

    /// Parse an integer, with an optional leading `-`.
    let pint =
        let label = "integer"

        let resultToInt (sign, digits) =
            let value = int digits

            match sign with
            | Some _ -> -value
            | None -> value

        opt (pchar '-') .>>. digits |> mapP resultToInt <?> label

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
