module Aoc.Parsing.Tests.OperatorsTests

open System

open Expecto

open Aoc.Parsing
open Aoc.Parsing.Tests.Helpers

let tests =
    testList "Operators" [
        testCase "<|> falls back to the right parser"
        <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a' <|> pchar 'b') "b")) 'b' "should pick 'b'"

        testCase "|>> maps the parsed value"
        <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a' |>> Char.ToUpper) "abc")) 'A' "should upper-case"

        testCase "<!> maps the parsed value"
        <| fun () -> Expect.equal (valueOf (Parser.run (Char.ToUpper <!> pchar 'a') "abc")) 'A' "should upper-case"

        testCase ".>>. pairs two parsers"
        <| fun () ->
            Expect.equal (valueOf (Parser.run (pchar 'a' .>>. pchar 'b') "ab")) ('a', 'b') "should pair the results"

        testCase ".>> keeps the left result"
        <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a' .>> pchar 'b') "ab")) 'a' "should keep 'a'"

        testCase ">>. keeps the right result"
        <| fun () -> Expect.equal (valueOf (Parser.run (pchar 'a' >>. pchar 'b') "ab")) 'b' "should keep 'b'"

        testCase "<*> applies a parsed function"
        <| fun () ->
            let parser = Parser.returnP Char.ToUpper <*> pchar 'a'
            Expect.equal (valueOf (Parser.run parser "abc")) 'A' "should apply the function"

        testCase ">>= chains parsers"
        <| fun () ->
            let parser = pchar 'a' >>= (fun a -> Parser.returnP (Char.ToUpper a))
            Expect.equal (valueOf (Parser.run parser "abc")) 'A' "should chain"

        testCase "<?> replaces the label"
        <| fun () ->
            let label, _, _ = failureOf (Parser.run (pchar 'a' <?> "the letter a") "b")
            Expect.equal label "the letter a" "should use the new label"
    ]
