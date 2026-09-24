import Aoc

private def check (name : String) (expected actual : Int) : IO Bool := do
  if actual == expected then
    IO.println s!"ok   {name}"
    return true
  else
    IO.println s!"FAIL {name}: expected {expected}, got {actual}"
    return false

def main : IO UInt32 := do
  let cases : List (String × Int × Int) :=
    [("part one example", 0, solvePartOne ""),
     ("part two example", 0, solvePartTwo "")]
  let results ← cases.mapM (fun (name, expected, actual) => check name expected actual)
  let failures := results.count false
  if failures == 0 then
    IO.println s!"{results.length} passed"
    return 0
  else
    IO.println s!"{failures} of {results.length} failed"
    return 1
