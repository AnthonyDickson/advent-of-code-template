package aoc

import arrow.core.Either
import arrow.core.raise.Raise
import arrow.core.raise.either
import arrow.core.raise.ensure
import kotlin.io.path.Path
import kotlin.io.path.readText
import kotlin.system.exitProcess
import kotlinx.collections.immutable.PersistentList
import kotlinx.collections.immutable.persistentListOf
import kotlinx.collections.immutable.toPersistentList

/** Everything that can stop a solution from producing an answer. */
sealed interface AocError {
    val message: String

    /** The input holds a character that is neither `(` nor `)`. */
    data class UnexpectedCharacter(val character: Char, val position: Int) : AocError {
        override val message = "unexpected character '$character' at position $position"
    }

    /** Santa never goes below the ground floor, so part two has no answer. */
    data object NeverEntersBasement : AocError {
        override val message = "Santa never enters the basement"
    }
}

/** One instruction: `(` goes up a floor and `)` goes down one. */
enum class Direction(val delta: Long) {
    Up(1),
    Down(-1),
}

/** Solves part one of the puzzle for the given input. */
fun solvePartOne(input: String): Either<AocError, Long> = either {
    parse(input).sumOf(Direction::delta)
}

/** Solves part two of the puzzle for the given input. */
fun solvePartTwo(input: String): Either<AocError, Long> = either {
    // `floors` starts with the ground floor, so the index of a floor is the position of the
    // instruction that led to it.
    val position = floors(parse(input)).indexOfFirst { floor -> floor < 0 }
    ensure(position >= 0) { AocError.NeverEntersBasement }
    position.toLong()
}

/** Reads the instructions, ignoring the trailing newline, and raises on anything else. */
private fun Raise<AocError>.parse(input: String): PersistentList<Direction> =
    input
        .trimEnd()
        .mapIndexed { index, character -> direction(character, index + 1) }
        .toPersistentList()

private fun Raise<AocError>.direction(character: Char, position: Int): Direction =
    when (character) {
        '(' -> Direction.Up
        ')' -> Direction.Down
        else -> raise(AocError.UnexpectedCharacter(character, position))
    }

/** Every floor Santa visits, starting on the ground floor. Each step adds to a persistent list. */
private fun floors(directions: PersistentList<Direction>): PersistentList<Long> =
    directions.fold(persistentListOf(0L)) { visited, direction ->
        visited.adding(visited.last() + direction.delta)
    }

/** Reads `input.txt`, prints both solutions one per line, and reports any error on stderr. */
fun main() {
    val input = Path("input.txt").readText()
    val answers = listOf(::solvePartOne, ::solvePartTwo).map { solve -> solve(input) }

    answers.forEach { answer ->
        answer.fold({ error -> System.err.println("error: ${error.message}") }, ::println)
    }
    if (answers.any(Either<AocError, Long>::isLeft)) exitProcess(1)
}
