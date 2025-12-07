import gleam/int
import gleam/io
import simplifile

pub fn main() -> Int {
  case simplifile.read("input.txt") {
    Ok(input) -> {
      input
      |> solve_part_one
      |> int.to_string
      |> io.println

      input
      |> solve_part_two
      |> int.to_string
      |> io.println

      0
    }
    Error(error) -> {
      io.println_error(
        "Could not load \"input.txt\": " <> simplifile.describe_error(error),
      )
      1
    }
  }
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
