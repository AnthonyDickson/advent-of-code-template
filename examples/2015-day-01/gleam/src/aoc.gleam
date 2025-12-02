import gleam/int
import gleam/io
import gleam/string
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

pub fn solve_part_one(input: String) -> Int {
  part_one_loop(0, string.to_graphemes(input))
}

fn part_one_loop(floor, chars) {
  case chars {
    [] -> floor
    ["(", ..tail] -> part_one_loop(floor + 1, tail)
    [_, ..tail] -> part_one_loop(floor - 1, tail)
  }
}

pub fn solve_part_two(input: String) -> Int {
  part_two_loop(0, 0, string.to_graphemes(input))
}

fn part_two_loop(floor, index, chars) {
  case chars {
    [] -> 1 + index
    ["(", ..tail] -> part_two_loop(floor + 1, index + 1, tail)
    [_, ..tail] ->
      case floor {
        0 -> 1 + index
        _ -> part_two_loop(floor - 1, index + 1, tail)
      }
  }
}
