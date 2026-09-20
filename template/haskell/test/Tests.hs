module Main (main) where

import Aoc (solvePartOne, solvePartTwo)
import Test.Tasty (TestTree, defaultMain, testGroup)
-- @?= is HUnit's equality assertion, re-exported by tasty-hunit:
-- `actual @?= expected` passes when the two values are equal and otherwise
-- fails the test, printing both values so the mismatch is easy to see.
import Test.Tasty.HUnit (testCase, (@?=))

main :: IO ()
main = defaultMain tests

tests :: TestTree
tests =
  testGroup
    "AoC"
    [ testGroup
        "Part One"
        [ testCase "example" $
            solvePartOne "" @?= 0
        ],
      testGroup
        "Part Two"
        [ testCase "example" $
            solvePartTwo "" @?= 0
        ]
    ]
