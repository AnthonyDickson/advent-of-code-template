module Main (main) where

import Aoc

main :: IO ()
main = do
  contents <- readFile "input.txt"
  print (solvePartOne contents)
  print (solvePartTwo contents)
