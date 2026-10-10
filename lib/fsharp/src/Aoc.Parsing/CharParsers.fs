namespace Aoc.Parsing

open System

/// Parsers for single characters and literal strings. Auto-opened with the
/// namespace, so `open Aoc.Parsing` is enough to use them.
[<AutoOpen>]
module CharParsers =
    open Parser
    open Operators

    /// Parse a specific character.
    let pchar charToMatch =
        let predicate ch = ch = charToMatch
        let label = $"'{charToMatch}'"
        satisfy predicate label

    /// Parse any one of a list of characters.
    let anyOf listOfChars =
        listOfChars
        |> List.map pchar
        |> choice
        |> setLabel (sprintf "anyOf %A" listOfChars)

    /// Convert a list of characters to a string.
    let charListToString charList = String(List.toArray charList)

    /// Parse zero or more characters with `parser` and return them as a string.
    let manyChars parser = many parser |>> charListToString

    /// Parse one or more characters with `parser` and return them as a string.
    let manyChars1 parser = many1 parser |>> charListToString

    /// Parse a specific string.
    ///
    /// Atomic: it either matches the whole string or fails without consuming
    /// any input, so `pstring "for" <|> pstring "foreach"` tries both. This
    /// matches FParsec's `pstring`, and means callers do not need to wrap a
    /// keyword in `attempt` to stop a partial match from committing.
    let pstring str =
        let label = $"'{str}'"

        let parser =
            str
            |> List.ofSeq
            |> List.map pchar
            |> sequence
            |> mapP charListToString
            |> attempt

        parser <?> label
