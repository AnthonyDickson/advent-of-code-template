module Aoc.Parsing.Tests.Main

open Expecto

[<Tests>]
let tests =
    testList "Aoc.Parsing" [
        Aoc.Parsing.Tests.PositionTests.tests
        Aoc.Parsing.Tests.ParserTests.tests
        Aoc.Parsing.Tests.OperatorsTests.tests
        Aoc.Parsing.Tests.CharParsersTests.tests
        Aoc.Parsing.Tests.WhitespaceParsersTests.tests
        Aoc.Parsing.Tests.NumericParsersTests.tests
    ]
