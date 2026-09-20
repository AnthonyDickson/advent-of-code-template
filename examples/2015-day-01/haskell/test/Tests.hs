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
    [ testGroup "Part One" (map partOneCase partOneCases),
      testGroup "Part Two" (map partTwoCase partTwoCases)
    ]

partOneCases :: [(String, Integer)]
partOneCases =
  [ ("(())", 0),
    ("()()", 0),
    ("(((", 3),
    ("(()(()(", 3),
    ("))(((((", 3),
    ("())", -1),
    ("))(", -1),
    (")))", -3),
    (")())())", -3)
  ]

partTwoCases :: [(String, Integer)]
partTwoCases =
  [ (")", 1),
    ("()())", 5)
  ]

partOneCase :: (String, Integer) -> TestTree
partOneCase (input, expected) = testCase (show input) $ solvePartOne input @?= expected

partTwoCase :: (String, Integer) -> TestTree
partTwoCase (input, expected) = testCase (show input) $ solvePartTwo input @?= expected
