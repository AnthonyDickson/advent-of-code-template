module Aoc.Parsing.Tests.WhitespaceParsersTests

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "WhitespaceParsers" [
        testCase "whitespaceChar parses a space"
        <| fun () -> Expect.equal (valueOf (Parser.run whitespaceChar " ")) ' ' "should parse the space"

        testCase "whitespaceChar parses a tab"
        <| fun () -> Expect.equal (valueOf (Parser.run whitespaceChar "\t")) '\t' "should parse the tab"

        testCase "whitespaceChar parses a newline"
        <| fun () -> Expect.equal (valueOf (Parser.run whitespaceChar "\n")) '\n' "should parse the newline"

        testCase "whitespaceChar fails on a letter"
        <| fun () ->
            let label, error, _ = failureOf (Parser.run whitespaceChar "a")
            Expect.equal label "whitespace" "should be labelled whitespace"
            Expect.equal error "Unexpected 'a'" "should describe the character"

        testCase "spaces parses zero or more whitespace characters"
        <| fun () ->
            let result = Parser.run spaces "   x"
            Expect.equal (valueOf result) [ ' '; ' '; ' ' ] "should parse every space"
            Expect.equal (remainingOf result).Position { Line = 0; Column = 3 } "should stop at the letter"

        testCase "spaces succeeds with an empty list"
        <| fun () -> Expect.equal (valueOf (Parser.run spaces "x")) [] "should parse nothing"

        testCase "spaces1 parses one or more whitespace characters"
        <| fun () -> Expect.equal (valueOf (Parser.run spaces1 "  x")) [ ' '; ' ' ] "should parse both spaces"

        testCase "spaces1 fails when there is no whitespace"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run spaces1 "x")
            Expect.equal label "many1 whitespace" "should label the failure"
    ]
