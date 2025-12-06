module Main where

import Aoc
import System.Exit (exitFailure)
import Test.HUnit

testPartOne :: Test
testPartOne = TestCase (assertEqual "Test Part One" expected actual)
  where
    expected = 0
    actual = solvePartOne ""

testPartTwo :: Test
testPartTwo = TestCase (assertEqual "Test Part Two" expected actual)
  where
    expected = 0
    actual = solvePartTwo ""

tests :: Test
tests =
  TestList
    [ TestLabel "Part One" testPartOne,
      TestLabel "Part Two" testPartTwo
    ]

main :: IO Counts
main = do
  counts <- runTestTT tests
  if failures counts > 0 then exitFailure else return counts
