defmodule Aoc do
  @moduledoc """
  Solutions for Advent of Code 2015, Day 1: Not Quite Lisp.
  """

  @doc """
  Solve part one of the AoC problem.

  Each `(` instruction takes Santa up one floor and each `)` takes him down one
  floor, so the answer is the floor he ends up on once every instruction has
  been followed.

  ## Examples

      iex> Aoc.solve_part_one("(())")
      0

      iex> Aoc.solve_part_one("(()(()(")
      3

      iex> Aoc.solve_part_one(")())())")
      -3

  """
  def solve_part_one(input) do
    input
    |> String.to_charlist()
    |> Enum.reduce(0, &step/2)
  end

  @doc """
  Solve part two of the AoC problem.

  The answer is the one-based position of the instruction that first takes
  Santa into the basement (floor `-1`). Returns `0` if the basement is never
  reached.

  ## Examples

      iex> Aoc.solve_part_two(")")
      1

      iex> Aoc.solve_part_two("()())")
      5

  """
  def solve_part_two(input) do
    input
    |> String.to_charlist()
    |> find_basement(0, 1)
  end

  defp find_basement([], _floor, _position), do: 0

  defp find_basement([char | rest], floor, position) do
    next_floor = step(char, floor)

    if next_floor == -1 do
      position
    else
      find_basement(rest, next_floor, position + 1)
    end
  end

  defp step(?\(, floor), do: floor + 1
  defp step(?\), floor), do: floor - 1
  defp step(char, _floor), do: raise("unexpected character: #{<<char>>}")
end
