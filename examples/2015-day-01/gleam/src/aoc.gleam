import gleam/int
import gleam/io
import gleam/list
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
  |> list.fold(0, fn(floor, char) { floor + step(char) })
}

pub fn solve_part_two(input: String) -> Int {
  let #(_, _, basement_index) =
    input
    |> string.to_graphemes
    |> list.fold(#(0, 0, 0), fn(state, char) {
      let #(floor, position, basement_index) = state
      let floor = floor + step(char)
      let position = position + 1
      let basement_index = case basement_index == 0 && floor == -1 {
        True -> position
        False -> basement_index
      }

      #(floor, position, basement_index)
    })

  basement_index
}

fn step(char: String) -> Int {
  case char {
    "(" -> 1
    ")" -> -1
    _ -> panic as "unexpected character, only '(' and ')' are allowed"
  }
}
