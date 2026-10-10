namespace Aoc.Parsing

open System

/// A line and column within the parsed input.
///
/// Both are zero based: `Line = 0` is the first line and `Column = 0` is the
/// first character of a line.
type Position = { Line : int; Column : int }

module Position =
    /// The position at the very start of the input.
    let zero = { Line = 0; Column = 0 }

    /// Move one column to the right.
    let incrementColumn position = {
        position with
            Column = position.Column + 1
    }

    /// Move to the start of the next line.
    let incrementLine position = {
        position with
            Line = position.Line + 1
            Column = 0
    }

/// The input being consumed, split into lines, together with the current
/// position. Splitting up front means a character can never straddle a line
/// break, and lines are exposed to error messages by index.
type InputState = {
    Lines : string[]
    Position : Position
}

module InputState =
    /// Build an input state from a string.
    ///
    /// Both `\r\n` and `\n` are treated as line endings, so input read on
    /// Windows and input read on Unix produce the same lines. A line ending at
    /// the very end of the input terminates the last line rather than starting
    /// an empty one, so `"a\n"` and `"a"` both produce the single line `"a"`
    /// (and `nextChar` reports one `'\n'` after it either way).
    let fromString (str : string) =
        if String.IsNullOrEmpty str then
            {
                Lines = [||]
                Position = Position.zero
            }
        else
            let separators = [| "\r\n"; "\n" |]
            let lines = str.Split (separators, StringSplitOptions.None)

            let lines =
                if lines.Length > 1 && lines.[lines.Length - 1] = "" then
                    lines.[.. lines.Length - 2]
                else
                    lines

            {
                Lines = lines
                Position = Position.zero
            }

    /// The line the current position points at, or `None` at the end of input.
    let currentLine inputState =
        let linePosition = inputState.Position.Line

        if linePosition < inputState.Lines.Length then
            Some inputState.Lines.[linePosition]
        else
            None

    /// Consume a single character, returning the state after it and the
    /// character itself, or `None` when there is no input left.
    ///
    /// The end of a line is reported as a `'\n'`, so a grammar does not need to
    /// special case line breaks.
    let nextChar inputState =
        let {
                Line = linePosition
                Column = columnPosition
            } =
            inputState.Position

        match currentLine inputState with
        | None -> inputState, None
        | Some currentLine ->
            if columnPosition < currentLine.Length then
                let next = currentLine.[columnPosition]
                let newPos = Position.incrementColumn inputState.Position
                let newState = { inputState with Position = newPos }
                newState, Some next
            else
                let next = '\n'
                let newPos = Position.incrementLine inputState.Position
                let newState = { inputState with Position = newPos }
                newState, Some next

/// A snapshot of where parsing stopped, used to build error messages. The
/// current line is included so a caller can show the offending line without
/// holding on to the whole input.
type ParserPosition = {
    CurrentLine : string option
    Line : int
    Column : int
}

module ParserPosition =
    /// Capture the position, and the line it sits on, from an input state.
    let fromInputState inputState = {
        CurrentLine = InputState.currentLine inputState
        Line = inputState.Position.Line
        Column = inputState.Position.Column
    }
