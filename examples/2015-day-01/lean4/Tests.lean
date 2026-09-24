import Aoc

private def check (name : String) (expected actual : Int) : IO Bool := do
  if actual == expected then
    IO.println s!"ok   {name}"
    return true
  else
    IO.println s!"FAIL {name}: expected {expected}, got {actual}"
    return false

private def partOneCases : List (String × Int) :=
  [("(())", 0),
   ("()()", 0),
   ("(((", 3),
   ("(()(()(", 3),
   ("))(((((", 3),
   ("())", -1),
   ("))(", -1),
   (")))", -3),
   (")())())", -3)]

private def partTwoCases : List (String × Int) :=
  [(")", 1), ("()())", 5)]

def main : IO UInt32 := do
  let one ← partOneCases.mapM (fun (input, expected) =>
    check s!"part one {input}" expected (solvePartOne input))
  let two ← partTwoCases.mapM (fun (input, expected) =>
    check s!"part two {input}" expected (solvePartTwo input))
  let outcomes := one ++ two
  let failures := outcomes.count false
  if failures == 0 then
    IO.println s!"{outcomes.length} passed"
    return 0
  else
    IO.println s!"{failures} of {outcomes.length} failed"
    return 1
