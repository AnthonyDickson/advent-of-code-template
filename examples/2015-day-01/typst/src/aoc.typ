// Day 1: Not Quite Lisp.
//
// `(` goes up one floor, `)` goes down one, and anything else leaves the floor
// where it is.

/// Moves one floor for a single instruction.
#let move(floor, instruction) = {
  if instruction == "(" { floor + 1 } else if instruction == ")" {
    floor - 1
  } else { floor }
}

/// Solves part one of the puzzle for `input`.
#let solve-part-one(input) = input.clusters().fold(0, move)

/// Solves part two of the puzzle for `input`.
#let solve-part-two(input) = {
  let floor = 0
  for (index, instruction) in input.clusters().enumerate() {
    floor = move(floor, instruction)
    if floor < 0 { return index + 1 }
  }
  0
}
