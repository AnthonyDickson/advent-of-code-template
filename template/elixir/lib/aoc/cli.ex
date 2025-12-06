defmodule Aoc.CLI do
  import Aoc

  def main(_args \\ []) do
    with {:ok, contents} <- File.read("input.txt") do
      IO.puts("#{solve_part_one(contents)}")
      IO.puts("#{solve_part_two(contents)}")
    end
  end
end
