module Aoc

let step floor instruction =
    match instruction with
    | '(' -> floor + 1
    | ')' -> floor - 1
    | _ -> invalidArg (nameof instruction) $"Invalid instruction '{instruction}', expected '(' or ')'"

/// Solves part one of the puzzle for the given input.
let solvePartOne (input : string) : int = input |> Seq.fold step 0

/// Solves part two of the puzzle for the given input.
let solvePartTwo (input : string) : int =
    input
    |> Seq.scan step 0
    |> Seq.skip 1
    |> Seq.tryFindIndex (fun floor -> floor = -1)
    |> Option.map (fun index -> index + 1)
    |> Option.defaultValue 0
