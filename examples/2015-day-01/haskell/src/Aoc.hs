module Aoc
  ( solvePartOne,
    solvePartTwo,
  )
where

import Data.List

step :: Integer -> Char -> Integer
step currentFloor '(' = currentFloor + 1
step currentFloor ')' = currentFloor - 1
step currentFloor _ = currentFloor

solvePartOne :: String -> Integer
solvePartOne = foldl' step 0

solvePartTwo :: String -> Integer
solvePartTwo = maybe 0 (fromIntegral . succ) . elemIndex (-1) . drop 1 . scanl step 0
