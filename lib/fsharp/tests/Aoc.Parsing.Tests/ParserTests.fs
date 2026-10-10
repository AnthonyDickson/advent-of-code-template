module Aoc.Parsing.Tests.ParserTests

open System

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "Parser" [
        testList "satisfy" [
            testCase "parses a matching character"
            <| fun () ->
                let result = Parser.run (satisfy ((=) 'a') "letter a") "abc"
                Expect.equal (valueOf result) 'a' "should parse the character"
                Expect.equal (remainingOf result).Position { Line = 0; Column = 1 } "should consume one character"

            testCase "fails on a non-matching character"
            <| fun () ->
                let label, error, position =
                    failureOf (Parser.run (satisfy ((=) 'a') "letter a") "xyz")

                Expect.equal label "letter a" "should keep the label"
                Expect.equal error "Unexpected 'x'" "should describe the offending character"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "xyz"
                        Line = 0
                        Column = 0
                    }
                    "should point at the failure"

            testCase "fails at the end of the input"
            <| fun () ->
                let _, error, position = failureOf (Parser.run (satisfy ((=) 'a') "letter a") "")
                Expect.equal error "No more input" "should report that input ran out"

                Expect.equal
                    position
                    {
                        CurrentLine = None
                        Line = 0
                        Column = 0
                    }
                    "should point at the end"
        ]

        testList "returnP" [
            testCase "succeeds without consuming input"
            <| fun () ->
                let result = Parser.run (Parser.returnP 42) "abc"
                Expect.equal (valueOf result) 42 "should return the value"
                Expect.equal (remainingOf result).Position Position.zero "should not consume input"
        ]

        testList "mapP" [
            testCase "transforms the parsed value"
            <| fun () ->
                let parser = pchar 'a' |> Parser.mapP Char.ToUpper
                Expect.equal (valueOf (Parser.run parser "abc")) 'A' "should upper-case the character"
        ]

        testList "orElse" [
            testCase "uses the first parser when it succeeds"
            <| fun () ->
                let parser = Parser.orElse (pchar 'a') (pchar 'b')
                Expect.equal (valueOf (Parser.run parser "abc")) 'a' "should pick the first match"

            testCase "falls back to the second parser"
            <| fun () ->
                let parser = Parser.orElse (pchar 'a') (pchar 'b')
                Expect.equal (valueOf (Parser.run parser "bcd")) 'b' "should pick the second match"

            testCase "reports the combined label"
            <| fun () ->
                let parser = Parser.orElse (pchar 'a') (pchar 'b')
                let label, _, _ = failureOf (Parser.run parser "xyz")
                Expect.equal label "'a' orElse 'b'" "should join the labels"
        ]

        testList "choice" [
            testCase "picks the first matching parser"
            <| fun () ->
                let parser = Parser.choice [ pchar 'a'; pchar 'b'; pchar 'c' ]
                Expect.equal (valueOf (Parser.run parser "cab")) 'c' "should pick the later match"

            testCase "reports every label when nothing matches"
            <| fun () ->
                let parser = Parser.choice [ pchar 'a'; pchar 'b'; pchar 'c' ]
                let label, _, _ = failureOf (Parser.run parser "xyz")
                Expect.equal label "'a' orElse 'b' orElse 'c'" "should join every label"
        ]

        testList "andThen" [
            testCase "pairs the results"
            <| fun () ->
                let result = Parser.run (Parser.andThen (pchar 'a') (pchar 'b')) "abc"
                Expect.equal (valueOf result) ('a', 'b') "should pair the characters"
                Expect.equal (remainingOf result).Position { Line = 0; Column = 2 } "should consume both"

            testCase "fails if the second parser fails"
            <| fun () ->
                let result = Parser.run (Parser.andThen (pchar 'a') (pchar 'b')) "axc"
                let _, error, position = failureOf result
                Expect.equal error "Unexpected 'x'" "should describe the second failure"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "axc"
                        Line = 0
                        Column = 1
                    }
                    "should point after the first parser"
        ]

        testList "applyP" [
            testCase "applies a parsed function"
            <| fun () ->
                let parser = Parser.applyP (Parser.returnP Char.ToUpper) (pchar 'a')
                Expect.equal (valueOf (Parser.run parser "abc")) 'A' "should apply the function"
        ]

        testList "lift2" [
            testCase "combines two parsers"
            <| fun () ->
                let parser = Parser.lift2 (fun a b -> sprintf "%c%c" a b) (pchar 'a') (pchar 'b')
                Expect.equal (valueOf (Parser.run parser "abc")) "ab" "should combine both results"
        ]

        testList "sequence" [
            testCase "turns parsers into a parser of a list"
            <| fun () ->
                let parser = Parser.sequence [ pchar 'a'; pchar 'b'; pchar 'c' ]
                Expect.equal (valueOf (Parser.run parser "abc")) [ 'a'; 'b'; 'c' ] "should collect every result"

            testCase "an empty list succeeds"
            <| fun () ->
                let parser = Parser.sequence ([]: Parser<char> list)
                Expect.equal (valueOf (Parser.run parser "abc")) [] "should return the empty list"
        ]

        testList "many" [
            testCase "matches zero or more occurrences"
            <| fun () ->
                let result = Parser.run (Parser.many (pchar 'a')) "aaab"
                Expect.equal (valueOf result) [ 'a'; 'a'; 'a' ] "should match every 'a'"
                Expect.equal (remainingOf result).Position { Line = 0; Column = 3 } "should stop at the first non-match"

            testCase "succeeds with an empty list when there is no match"
            <| fun () ->
                let result = Parser.run (Parser.many (pchar 'a')) "bbb"
                Expect.equal (valueOf result) [] "should match nothing"
                Expect.equal (remainingOf result).Position Position.zero "should not consume input"
        ]

        testList "many1" [
            testCase "matches one or more occurrences"
            <| fun () ->
                let result = Parser.run (Parser.many1 (pchar 'a')) "aab"
                Expect.equal (valueOf result) [ 'a'; 'a' ] "should match every 'a'"

            testCase "fails when nothing matches"
            <| fun () ->
                let result = Parser.run (Parser.many1 (pchar 'a')) "bbb"
                let label, error, position = failureOf result
                Expect.equal label "many1 'a'" "should label the failure"
                Expect.equal error "Unexpected 'b'" "should describe the offending character"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "bbb"
                        Line = 0
                        Column = 0
                    }
                    "should point at the start"
        ]

        testList "opt" [
            testCase "matches a present value"
            <| fun () ->
                let actual = valueOf (Parser.run (Parser.opt (pchar 'a')) "abc")
                Expect.equal actual (Some 'a') "should wrap the value"

            testCase "succeeds with None when absent"
            <| fun () ->
                let result = Parser.run (Parser.opt (pchar 'a')) "xyz"
                Expect.equal (valueOf result) None "should return None"
                Expect.equal (remainingOf result).Position Position.zero "should not consume input"
        ]

        testList "keepLeft and keepRight" [
            testCase "keepLeft keeps the left result"
            <| fun () ->
                let parser = Parser.keepLeft (pchar 'a') (pchar 'b')
                Expect.equal (valueOf (Parser.run parser "ab")) 'a' "should keep 'a'"

            testCase "keepRight keeps the right result"
            <| fun () ->
                let parser = Parser.keepRight (pchar 'a') (pchar 'b')
                Expect.equal (valueOf (Parser.run parser "ab")) 'b' "should keep 'b'"
        ]

        testList "between" [
            testCase "keeps the middle parser"
            <| fun () ->
                let parser = Parser.between (pchar '[') (pstring "ab") (pchar ']')
                Expect.equal (valueOf (Parser.run parser "[ab]")) "ab" "should keep the middle"
        ]

        testList "sepBy and sepBy1" [
            testCase "sepBy1 parses one or more separated values"
            <| fun () ->
                let parser = Parser.sepBy1 (pchar 'a') (pchar ',')
                Expect.equal (valueOf (Parser.run parser "a,a,a")) [ 'a'; 'a'; 'a' ] "should parse every value"

            testCase "sepBy1 fails when there is no value"
            <| fun () ->
                let parser = Parser.sepBy1 (pchar 'a') (pchar ',')
                let _, error, position = failureOf (Parser.run parser "b")
                Expect.equal error "Unexpected 'b'" "should report the element parser's error"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "b"
                        Line = 0
                        Column = 0
                    }
                    "should point at the input"

            testCase "sepBy parses zero or more separated values"
            <| fun () ->
                let parser = Parser.sepBy (pchar 'a') (pchar ',')
                Expect.equal (valueOf (Parser.run parser "a,a")) [ 'a'; 'a' ] "should parse every value"

            testCase "sepBy succeeds with an empty list when there is no value"
            <| fun () ->
                let parser = Parser.sepBy (pchar 'a') (pchar ',')
                Expect.equal (valueOf (Parser.run parser "b")) [] "should parse nothing"
        ]

        testList "run and runOnInputState" [
            testCase "run starts at the beginning of the input"
            <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a') "abc")) 'a' "should parse from the start"

            testCase "runOnInputState parses from a given state"
            <| fun () ->
                let reply = Parser.runOnInputState (pchar 'b') (inputAt "abc" 0 1)
                Expect.equal (valueOf reply.Outcome) 'b' "should parse from the given state"
        ]

        testList "labels" [
            testCase "getLabel returns the parser's label"
            <| fun () -> Expect.equal (Parser.getLabel (pchar 'a')) "'a'" "should return the label"

            testCase "setLabel replaces the failure label"
            <| fun () ->
                let parser = Parser.setLabel "the letter a" (pchar 'a')
                let label, _, _ = failureOf (Parser.run parser "b")
                Expect.equal label "the letter a" "should use the new label"
        ]

        testList "ParseResult.toDisplayString" [
            testCase "renders a success"
            <| fun () ->
                let result = Success(42, InputState.fromString "")
                Expect.equal (ParseResult.toDisplayString result) "42" "should render the value"

            testCase "renders a failure with a caret"
            <| fun () ->
                let position = {
                    CurrentLine = Some "ax"
                    Line = 2
                    Column = 1
                }

                let result = Failure("integer", "Unexpected 'x'", position)

                Expect.equal
                    (ParseResult.toDisplayString result)
                    "Line:2 Col:1 Error parsing integer\nax\n ^Unexpected 'x'"
                    "should render the position, the line and a caret"
        ]

        testList "error positions" [
            testCase "point at the line and column after the consumed input"
            <| fun () ->
                let parser = Parser.andThen (pstring "ab\n") (pchar 'q')
                let _, error, position = failureOf (Parser.run parser "ab\ncd")
                Expect.equal error "Unexpected 'c'" "should describe the offending character"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "cd"
                        Line = 1
                        Column = 0
                    }
                    "should point at the second line"
        ]

        testList "committed failure" [
            testCase "orElse does not backtrack when the first parser consumed input"
            <| fun () ->
                let first = Parser.keepLeft (pchar 'a') (pchar 'b')
                let parser = Parser.orElse first (pchar 'a')
                let _, error, position = failureOf (Parser.run parser "ax")
                Expect.equal error "Unexpected 'x'" "should keep the committed failure"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "ax"
                        Line = 0
                        Column = 1
                    }
                    "should point at the offending character, not the start"

            testCase "attempt lets the alternative backtrack"
            <| fun () ->
                let first = Parser.attempt (Parser.keepLeft (pchar 'a') (pchar 'b'))
                let parser = Parser.orElse first (pchar 'a')
                Expect.equal (valueOf (Parser.run parser "ax")) 'a' "should fall back to the first character"

            testCase "tryP is an alias for attempt"
            <| fun () ->
                let first = Parser.tryP (Parser.keepLeft (pchar 'a') (pchar 'b'))
                let parser = Parser.orElse first (pchar 'a')
                Expect.equal (valueOf (Parser.run parser "ax")) 'a' "should fall back to the first character"

            testCase "many propagates a committed element failure"
            <| fun () ->
                let element = Parser.keepLeft (pchar 'a') (pchar 'b')
                let _, error, position = failureOf (Parser.run (Parser.many element) "abax")
                Expect.equal error "Unexpected 'x'" "should report the committed element failure"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "abax"
                        Line = 0
                        Column = 3
                    }
                    "should point at the committed failure"

            testCase "sepBy propagates a trailing separator"
            <| fun () ->
                let parser = Parser.sepBy (pchar 'a') (pchar ',')
                let _, error, position = failureOf (Parser.run parser "a,a,")
                Expect.equal error "Unexpected '\n'" "should fail rather than stop at the trailing separator"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "a,a,"
                        Line = 0
                        Column = 4
                    }
                    "should point past the last separator"

            testCase "opt propagates a committed failure instead of returning None"
            <| fun () ->
                let parser = Parser.opt (Parser.andThen (pchar 'a') (pchar 'b'))
                let _, error, _ = failureOf (Parser.run parser "ax")
                Expect.equal error "Unexpected 'x'" "should not swallow the committed failure"

            testCase "many raises on a parser that accepts empty input"
            <| fun () ->
                let parser = Parser.many (Parser.returnP 'x')
                Expect.throws (fun () -> Parser.run parser "abc" |> ignore) "should raise the guard error"
        ]

        testList "runReply" [
            testCase "reports whether input was consumed"
            <| fun () ->
                Expect.equal (Parser.runReply (pchar 'a') "abc").Consumed Consumed "should report consumption"

                Expect.equal
                    (Parser.runReply (pchar 'a') "xyz").Consumed
                    NotConsumed
                    "should report no consumption on a soft failure"
        ]

        testList "eof" [
            testCase "succeeds at the end of the input"
            <| fun () -> Expect.equal (valueOf (Parser.run eof "")) () "should accept the end of the input"

            testCase "fails without consuming when input remains"
            <| fun () ->
                let label, error, position = failureOf (Parser.run eof "ab")
                Expect.equal label "end of input" "should label the failure"
                Expect.equal error "Expected end of input" "should describe the trailing input"

                Expect.equal
                    position
                    {
                        CurrentLine = Some "ab"
                        Line = 0
                        Column = 0
                    }
                    "should point at the remaining input"

            testCase "succeeds once the input, including its line break, is consumed"
            <| fun () ->
                let parser = pchar 'a' .>> pchar '\n' .>> eof
                Expect.equal (valueOf (Parser.run parser "a")) 'a' "should accept the end of the input"

            testCase "succeeds after the final line break of input that ends with one"
            <| fun () ->
                let parser = pchar 'a' .>> pchar '\n' .>> eof
                Expect.equal (valueOf (Parser.run parser "a\n")) 'a' "should not report an extra line break"
        ]
    ]
