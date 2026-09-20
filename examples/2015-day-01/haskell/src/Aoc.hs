module Aoc
  ( solvePartOne,
    solvePartTwo,
  )
where

step :: Integer -> Char -> Integer
step currentFloor '(' = currentFloor + 1
step currentFloor ')' = currentFloor - 1
step _ char = error ("unexpected char: " ++ show char)

solvePartOne :: String -> Integer
solvePartOne = foldl' step 0

solvePartTwo :: String -> Integer
solvePartTwo = findBasement 0 1
  where
    findBasement :: Integer -> Integer -> String -> Integer
    findBasement _ _ [] = 0
    findBasement currentFloor index (char : rest)
      | nextFloor == -1 = index
      | otherwise = findBasement nextFloor (index + 1) rest
      where
        nextFloor = step currentFloor char
