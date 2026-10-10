import gleam/int
import gleam/io
import simplifile

pub fn main() -> Nil {
  let input = case simplifile.read("input.txt") {
    Ok(input) -> input
    Error(error) ->
      panic as {
        "Could not load \"input.txt\": " <> simplifile.describe_error(error)
      }
  }

  input
  |> solve_part_one
  |> int.to_string
  |> io.println

  input
  |> solve_part_two
  |> int.to_string
  |> io.println
}

pub fn solve_part_one(_input: String) -> Int {
  0
}

pub fn solve_part_two(_input: String) -> Int {
  0
}
