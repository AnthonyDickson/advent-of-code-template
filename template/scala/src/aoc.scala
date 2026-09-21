import scala.io.Source

/** Solves part one of the puzzle for the given input. */
def solvePartOne(input: String): Long = 0

/** Solves part two of the puzzle for the given input. */
def solvePartTwo(input: String): Long = 0

@main def aoc(): Unit =
  val input = Source.fromFile("input.txt").mkString

  println(solvePartOne(input))
  println(solvePartTwo(input))
