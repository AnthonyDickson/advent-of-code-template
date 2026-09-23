import gleam/int
import gleam/io
import gleam/list
import gleam/result
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
  input
  |> string.to_graphemes
  |> list.fold(0, step)
}

pub fn solve_part_two(input: String) -> Int {
  input
  |> string.to_graphemes
  |> list.scan(0, step)
  |> list.index_map(fn(floor, index) { #(index, floor) })
  |> list.find(fn(pair) { pair.1 == -1 })
  |> result.map(fn(pair) { pair.0 + 1 })
  |> result.unwrap(0)
}

fn step(floor: Int, char: String) -> Int {
  case char {
    "(" -> floor + 1
    ")" -> floor - 1
    _ -> floor
  }
}
