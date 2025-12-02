import gleam/int
import gleam/io

pub fn main() -> Nil {
  let input = load_input("input.txt")

  input
  |> solve_part_one
  |> int.to_string
  |> io.println

  input
  |> solve_part_two
  |> int.to_string
  |> io.println
}

pub fn load_input(_filename: String) -> String {
  ""
}

pub fn solve_part_one(_input: String) -> Int {
  0
}

pub fn solve_part_two(_input: String) -> Int {
  0
}
