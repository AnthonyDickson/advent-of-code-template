module Main (main) where

import Aoc
import System.IO

main :: IO ()
main = do
  handle <- openFile "input.txt" ReadMode
  contents <- hGetContents handle
  print (solvePartOne contents)
  print (solvePartTwo contents)
