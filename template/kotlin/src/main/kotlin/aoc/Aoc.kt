package aoc

import kotlin.io.path.Path
import kotlin.io.path.readText

/** Solves part one of the puzzle for the given input. */
fun solvePartOne(input: String): Long = 0

/** Solves part two of the puzzle for the given input. */
fun solvePartTwo(input: String): Long = 0

/** Reads `input.txt` and prints both solutions, one per line. */
fun main() {
    val input = Path("input.txt").readText()

    listOf(::solvePartOne, ::solvePartTwo).map { solve -> solve(input) }.forEach(::println)
}
