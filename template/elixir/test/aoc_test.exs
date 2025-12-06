defmodule AocTest do
  use ExUnit.Case
  doctest Aoc

  test "solves part one" do
    assert Aoc.solve_part_one("") == 0
  end

  test "solves part two" do
    assert Aoc.solve_part_two("") == 0
  end
end
