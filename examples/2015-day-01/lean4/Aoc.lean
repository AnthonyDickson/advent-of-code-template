private def step (floor : Int) (c : Char) : Int :=
  match c with
  | '(' => floor + 1
  | ')' => floor - 1
  | _ => floor

private def firstBasement (floor : Int) (position : Nat) : List Char → Int
  | [] => 0
  | c :: rest =>
    let next := step floor c
    if next == -1 then (position : Int) + 1 else firstBasement next (position + 1) rest

def solvePartOne (input : String) : Int :=
  input.toList.foldl step 0

def solvePartTwo (input : String) : Int :=
  firstBasement 0 0 input.toList
