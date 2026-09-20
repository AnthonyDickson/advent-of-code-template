defmodule Aoc.CLI do
  @moduledoc """
  Command line entry point for the Advent of Code solutions.
  """

  alias Aoc

  def main(_args \\ []) do
    case File.read("input.txt") do
      {:ok, contents} ->
        IO.puts(Aoc.solve_part_one(contents))
        IO.puts(Aoc.solve_part_two(contents))

      {:error, reason} ->
        IO.puts(:stderr, "Could not read input.txt: #{:file.format_error(reason)}")
        System.halt(1)
    end
  end
end
