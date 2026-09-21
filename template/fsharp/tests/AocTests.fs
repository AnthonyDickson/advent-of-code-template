namespace Aoc.Tests

open Expecto

open Aoc

module AocTests =
    /// Checks one solution function against the example in the puzzle statement.
    let private checkSolution (solve : string -> int) (input : string) (expected : int) =
        let actual = solve input

        Expect.equal actual expected (sprintf "failed on input %A" input)

    [<Tests>]
    let aocTests =
        testList "Aoc" [
            testList "Part One" [ testCase "example" <| fun () -> checkSolution solvePartOne "" 0 ]

            testList "Part Two" [ testCase "example" <| fun () -> checkSolution solvePartTwo "" 0 ]
        ]
