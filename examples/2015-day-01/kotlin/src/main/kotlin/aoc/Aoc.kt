package aoc

import kotlin.io.path.Path
import kotlin.io.path.readText

/** Solves part one of the puzzle for the given input. */
fun solvePartOne(input: String): Long = input.fold(0L, ::move)

/** Solves part two of the puzzle for the given input. */
fun solvePartTwo(input: String): Long =
    input.scan(0L, ::move).withIndex().firstOrNull { (_, floor) -> floor < 0 }?.index?.toLong() ?: 0

private fun move(floor: Long, character: Char): Long =
    when (character) {
        '(' -> floor + 1
        ')' -> floor - 1
        else -> floor
    }

/** Reads `input.txt` and prints both solutions one per line. */
fun main() {
    val input = Path("input.txt").readText()

    println(solvePartOne(input))
    println(solvePartTwo(input))
}
