import aoc
import gleam/int
import gleam/list
import gleeunit

pub fn main() -> Nil {
  gleeunit.main()
}

/// Checks `solve` against every example in the puzzle statement.
fn check(cases: List(#(String, Int)), solve: fn(String) -> Int) {
  list.each(cases, fn(case_) {
    let #(input, expected) = case_
    let actual = solve(input)

    assert actual == expected
      as {
        "Expected input \""
        <> input
        <> "\" to return "
        <> int.to_string(expected)
        <> ", got "
        <> int.to_string(actual)
      }
  })
}

pub fn part_one_test() {
  check(
    [
      #("(())", 0),
      #("()()", 0),
      #("(((", 3),
      #("(()(()(", 3),
      #("))(((((", 3),
      #("())", -1),
      #("))(", -1),
      #(")))", -3),
      #(")())())", -3),
    ],
    aoc.solve_part_one,
  )
}

pub fn part_two_test() {
  check(
    [
      #(")", 1),
      #("()())", 5),
    ],
    aoc.solve_part_two,
  )
}
