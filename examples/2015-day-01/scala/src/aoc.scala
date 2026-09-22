import scala.io.Source

/** Solves part one of the puzzle for the given input. */
def solvePartOne(input: String): Long = input.foldLeft(0L)(move)

/** Solves part two of the puzzle for the given input. */
def solvePartTwo(input: String): Long =
  input.iterator
    .scanLeft(0L)(move)
    .zipWithIndex
    .collectFirst { case (floor, index) if floor < 0 => index.toLong }
    .getOrElse(0L)

/** `(` goes up one floor, `)` goes down one, and anything else leaves the floor alone. */
private def move(floor: Long, char: Char): Long =
  char match
    case '(' => floor + 1
    case ')' => floor - 1
    case _   => floor

@main def aoc(): Unit =
  val input = Source.fromFile("input.txt").mkString

  println(solvePartOne(input))
  println(solvePartTwo(input))
