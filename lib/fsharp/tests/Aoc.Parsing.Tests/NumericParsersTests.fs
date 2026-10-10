module Aoc.Parsing.Tests.NumericParsersTests

open System

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

        testCase "pint fails, rather than throwing, when the integer is out of range"
        <| fun () ->
            let reply = Parser.runOnInputState pint (inputAt "99999999999" 0 0)
            Expect.equal reply.Consumed Consumed "should commit to the digits it read"
            let label, error, position = failureOf reply.Outcome
            Expect.equal label "integer" "should be labelled integer"
            Expect.equal error "99999999999 is out of range" "should name the number"
            Expect.equal (position.Line, position.Column) (0, 0) "should point at the start of the number"

        testCase "pint parses the smallest 32-bit integer"
        <| fun () -> Expect.equal (valueOf (Parser.run pint "-2147483648")) Int32.MinValue "should parse the minimum"

        testCase "pint64 parses an integer beyond 32 bits"
        <| fun () -> Expect.equal (valueOf (Parser.run pint64 "99999999999")) 99999999999L "should parse the integer"

        testCase "pint64 parses a negative integer"
        <| fun () -> Expect.equal (valueOf (Parser.run pint64 "-45")) -45L "should parse the sign"

        testCase "digitChar rejects non-ASCII digits"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run digitChar "٣")
            Expect.equal label "digit" "should be labelled digit"

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
