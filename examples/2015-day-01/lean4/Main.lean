import Aoc

def main : IO Unit := do
  let input ← IO.FS.readFile "input.txt"
  IO.println (solvePartOne input)
  IO.println (solvePartTwo input)
