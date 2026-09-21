namespace Aoc.Tests

open Expecto

open Aoc

module AocTests =
    let private partOneCases = [
        "(())", 0
        "()()", 0
        "(((", 3
        "(()(()(", 3
        "))(((((", 3
        "())", -1
        "))(", -1
        ")))", -3
        ")())())", -3
    ]

    let private partTwoCases = [ ")", 1; "()())", 5 ]

    /// Checks one solution function against the example in the puzzle statement.
    let private checkSolution (solve : string -> int) (input : string) (expected : int) =
        let actual = solve input

        Expect.equal actual expected (sprintf "failed on input %A" input)

    [<Tests>]
    let aocTests =
        testList "Aoc" [
            testList
                "Part One"
                (List.mapi
                    (fun index (input, answer) ->
                        testCase $"Example {index + 1}"
                        <| fun () -> checkSolution solvePartOne input answer)
                    partOneCases)
            testList
                "Part Two"
                (List.mapi
                    (fun index (input, answer) ->
                        testCase $"Example {index + 1}"
                        <| fun () -> checkSolution solvePartTwo input answer)
                    partTwoCases)
        ]
