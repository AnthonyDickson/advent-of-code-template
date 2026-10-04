module Aoc.Parsing.Tests.Helpers

open Expecto

open Aoc.Parsing

/// Extract the value from a successful parse, failing the test on a failure.
let valueOf result =
    match result with
    | Success (value, _) -> value
    | Failure (label, error, position) ->
        failtestf "expected a success but got a failure labelled %s: %s at %A" label error position

/// Extract the remaining input from a successful parse.
let remainingOf result =
    match result with
    | Success (_, input) -> input
    | Failure (label, error, position) ->
        failtestf "expected a success but got a failure labelled %s: %s at %A" label error position

/// Extract the label, error and position from a failed parse.
let failureOf result =
    match result with
    | Success (value, _) -> failtestf "expected a failure but parsed %A" value
    | Failure (label, error, position) -> label, error, position

/// Build an input state from `content`, positioned at the given line and column.
let inputAt content line column = {
    InputState.fromString content with
        Position = { Line = line; Column = column }
}
