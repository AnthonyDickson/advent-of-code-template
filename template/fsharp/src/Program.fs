module Program

open System.IO

open Aoc

[<EntryPoint>]
let main _ =
    let input = File.ReadAllText "input.txt"

    printfn "%d" (solvePartOne input)
    printfn "%d" (solvePartTwo input)

    0
