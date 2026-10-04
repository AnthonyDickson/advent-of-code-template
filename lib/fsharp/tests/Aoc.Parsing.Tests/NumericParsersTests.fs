module Aoc.Parsing.Tests.NumericParsersTests

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "NumericParsers" [
        testCase "digitChar parses a digit"
        <| fun () -> Expect.equal (valueOf (Parser.run digitChar "5")) '5' "should parse the digit"

        testCase "digitChar fails on a letter"
        <| fun () ->
            let label, error, _ = failureOf (Parser.run digitChar "a")
            Expect.equal label "digit" "should be labelled digit"
            Expect.equal error "Unexpected 'a'" "should describe the character"

        testCase "digits parses a run of digits"
        <| fun () -> Expect.equal (valueOf (Parser.run digits "123a")) "123" "should parse every digit"

        testCase "digits fails when there is no digit"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run digits "abc")
            Expect.equal label "many1 digit" "should label the failure"

        testCase "pint parses a positive integer"
        <| fun () ->
            let result = Parser.run pint "123abc"
            Expect.equal (valueOf result) 123 "should parse the integer"
            Expect.equal (remainingOf result).Position { Line = 0; Column = 3 } "should stop after the digits"

        testCase "pint parses a negative integer"
        <| fun () -> Expect.equal (valueOf (Parser.run pint "-45")) -45 "should parse the sign"

        testCase "pint parses zero"
        <| fun () -> Expect.equal (valueOf (Parser.run pint "0")) 0 "should parse zero"

        testCase "pint fails when there is no digit"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run pint "abc")
            Expect.equal label "integer" "should be labelled integer"

        testCase "pfloat parses a float"
        <| fun () ->
            let actual = valueOf (Parser.run pfloat "3.14")
            Expect.floatClose Accuracy.veryHigh actual 3.14 "should parse the float"

        testCase "pfloat parses a negative float"
        <| fun () ->
            let actual = valueOf (Parser.run pfloat "-2.5")
            Expect.floatClose Accuracy.veryHigh actual -2.5 "should parse the sign"

        testCase "pfloat fails without a fractional part"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run pfloat "3")
            Expect.equal label "float" "should be labelled float"
    ]
