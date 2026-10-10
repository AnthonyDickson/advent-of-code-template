module Aoc.Parsing.Tests.PositionTests

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "Position" [
        testCase "zero is the origin"
        <| fun () -> Expect.equal Position.zero { Line = 0; Column = 0 } "zero should be the origin"

        testCase "incrementColumn advances the column only"
        <| fun () ->
            let actual = Position.incrementColumn { Line = 2; Column = 5 }
            Expect.equal actual { Line = 2; Column = 6 } "should leave the line alone"

        testCase "incrementLine advances the line and resets the column"
        <| fun () ->
            let actual = Position.incrementLine { Line = 2; Column = 5 }
            Expect.equal actual { Line = 3; Column = 0 } "should reset the column"

        testList "InputState.fromString" [
            testCase "an empty string has no lines"
            <| fun () ->
                let actual = InputState.fromString ""
                Expect.sequenceEqual actual.Lines [||] "should have no lines"
                Expect.equal actual.Position Position.zero "should start at zero"

            testCase "splits on \\n"
            <| fun () ->
                let actual = InputState.fromString "ab\ncd"
                Expect.sequenceEqual actual.Lines [| "ab"; "cd" |] "should split into two lines"
                Expect.equal actual.Position Position.zero "should start at zero"

            testCase "splits on \\r\\n"
            <| fun () ->
                let actual = InputState.fromString "ab\r\ncd"
                Expect.sequenceEqual actual.Lines [| "ab"; "cd" |] "should strip the carriage return"

            testCase "a trailing line ending does not add an empty line"
            <| fun () ->
                let actual = InputState.fromString "ab\ncd\n"
                Expect.sequenceEqual actual.Lines [| "ab"; "cd" |] "should end on the last line"

            testCase "a trailing \\r\\n does not add an empty line"
            <| fun () ->
                let actual = InputState.fromString "ab\r\n"
                Expect.sequenceEqual actual.Lines [| "ab" |] "should end on the last line"

            testCase "keeps blank lines before the trailing line ending"
            <| fun () ->
                let actual = InputState.fromString "ab\n\n"
                Expect.sequenceEqual actual.Lines [| "ab"; "" |] "should keep the blank line"

            testCase "a lone line ending is one empty line"
            <| fun () ->
                let actual = InputState.fromString "\n"
                Expect.sequenceEqual actual.Lines [| "" |] "should have one empty line"
        ]

        testList "InputState.currentLine" [
            testCase "returns the current line"
            <| fun () ->
                let actual = InputState.currentLine (inputAt "ab\ncd" 1 0)
                Expect.equal actual (Some "cd") "should return the second line"

            testCase "returns None past the last line"
            <| fun () ->
                let actual = InputState.currentLine (inputAt "ab" 1 0)
                Expect.isNone actual "should return no line"
        ]

        testList "InputState.nextChar" [
            testCase "returns the next character and advances the column"
            <| fun () ->
                let next, charOpt = InputState.nextChar (inputAt "ab" 0 0)
                Expect.equal charOpt (Some 'a') "should return the first character"
                Expect.equal next.Position { Line = 0; Column = 1 } "should advance the column"

            testCase "reports the end of a line as a newline"
            <| fun () ->
                let next, charOpt = InputState.nextChar (inputAt "ab" 0 2)
                Expect.equal charOpt (Some '\n') "should report a newline"
                Expect.equal next.Position { Line = 1; Column = 0 } "should move to the next line"

            testCase "returns None at the end of the input"
            <| fun () ->
                let next, charOpt = InputState.nextChar (inputAt "ab" 1 0)
                Expect.isNone charOpt "should return no character"
                Expect.equal next (inputAt "ab" 1 0) "should not advance"
        ]

        testList "ParserPosition.fromInputState" [
            testCase "captures the current line and position"
            <| fun () ->
                let actual = ParserPosition.fromInputState (inputAt "ab\ncd" 1 1)

                Expect.equal
                    actual
                    {
                        CurrentLine = Some "cd"
                        Line = 1
                        Column = 1
                    }
                    "should capture the position"

            testCase "has no current line at the end of the input"
            <| fun () ->
                let actual = ParserPosition.fromInputState (inputAt "ab" 1 0)

                Expect.equal
                    actual
                    {
                        CurrentLine = None
                        Line = 1
                        Column = 0
                    }
                    "should have no line"
        ]
    ]
