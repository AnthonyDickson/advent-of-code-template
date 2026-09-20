defmodule AocTest do
  use ExUnit.Case
  doctest Aoc

  @part_one_examples [
    {"(())", 0},
    {"()()", 0},
    {"(((", 3},
    {"(()(()(", 3},
    {"))(((((", 3},
    {"())", -1},
    {"))(", -1},
    {")))", -3},
    {")())())", -3}
  ]

  @part_two_examples [
    {")", 1},
    {"()())", 5}
  ]

  test "solves part one" do
    for {input, expected} <- @part_one_examples do
      assert Aoc.solve_part_one(input) == expected,
             "failed for input #{inspect(input)}"
    end
  end

  test "solves part two" do
    for {input, expected} <- @part_two_examples do
      assert Aoc.solve_part_two(input) == expected,
             "failed for input #{inspect(input)}"
    end
  end
end
