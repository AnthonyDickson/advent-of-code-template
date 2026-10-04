module Aoc.Parsing.Tests.CharParsersTests

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "CharParsers" [
        testCase "pchar parses the matching character"
        <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a') "abc")) 'a' "should parse 'a'"

        testCase "pchar labels the parser with the character"
        <| fun () -> Expect.equal (Parser.getLabel (pchar 'a')) "'a'" "should label with the character"

        testCase "pchar fails on a different character"
        <| fun () ->
            let label, error, _ = failureOf (Parser.run (pchar 'a') "b")
            Expect.equal label "'a'" "should use the character as the label"
            Expect.equal error "Unexpected 'b'" "should describe the character"

        testCase "anyOf parses any listed character"
        <| fun () -> Expect.equal (valueOf (Parser.run (anyOf [ 'a'; 'b'; 'c' ]) "b")) 'b' "should parse 'b'"

        testCase "anyOf fails on an unlisted character"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run (anyOf [ 'a'; 'b' ]) "z")
            Expect.equal label "anyOf ['a'; 'b']" "should list the accepted characters"

        testCase "manyChars parses zero or more characters"
        <| fun () -> Expect.equal (valueOf (Parser.run (manyChars (pchar 'a')) "aab")) "aa" "should parse both 'a's"

        testCase "manyChars succeeds with an empty string"
        <| fun () -> Expect.equal (valueOf (Parser.run (manyChars (pchar 'a')) "b")) "" "should parse nothing"

        testCase "manyChars1 parses one or more characters"
        <| fun () -> Expect.equal (valueOf (Parser.run (manyChars1 (pchar 'a')) "aab")) "aa" "should parse both 'a's"

        testCase "manyChars1 fails when nothing matches"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run (manyChars1 (pchar 'a')) "b")
            Expect.equal label "many1 'a'" "should label the failure"

        testCase "charListToString joins characters"
        <| fun () -> Expect.equal (charListToString [ 'a'; 'b' ]) "ab" "should join the characters"

        testCase "pstring parses the whole string"
        <| fun () ->
            let result = Parser.run (pstring "hello") "hello world"
            Expect.equal (valueOf result) "hello" "should parse the string"
            Expect.equal (remainingOf result).Position { Line = 0; Column = 5 } "should consume the string"

        testCase "pstring fails part-way through"
        <| fun () ->
            let label, error, position = failureOf (Parser.run (pstring "hello") "help!")
            Expect.equal label "'hello'" "should label with the string"
            Expect.equal error "Unexpected 'p'" "should describe the mismatched character"

            Expect.equal
                position
                {
                    CurrentLine = Some "help!"
                    Line = 0
                    Column = 3
                }
                "should point at the mismatch"
    ]
