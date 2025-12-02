import aoc
import gleam/int
import gleam/list
import gleeunit

pub fn main() -> Nil {
  gleeunit.main()
}

pub fn part_one_test() {
  let cases = [
    #("(())", 0),
    #("()()", 0),
    #("(((", 3),
    #("(()(()(", 3),
    #("))(((((", 3),
    #("())", -1),
    #("))(", -1),
    #(")))", -3),
    #(")())())", -3),
  ]

  list.each(cases, fn(case_) {
    let #(input, expected) = case_

    let actual = aoc.solve_part_one(input)
    assert actual == expected
      as {
        "Expected input \""
        <> input
        <> "\" to return "
        <> int.to_string(expected)
      }
  })
}

pub fn part_two_test() {
  let cases = [
    #(")", 1),
    #("()())", 5),
  ]

  list.each(cases, fn(case_) {
    let #(input, expected) = case_

    let actual = aoc.solve_part_two(input)
    assert actual == expected
      as {
        "Expected input \""
        <> input
        <> "\" to return "
        <> int.to_string(expected)
      }
  })
}
