package aoc

import arrow.core.Either
import arrow.core.left
import arrow.core.right
import kotlin.test.Test
import kotlin.test.assertEquals

class AocTest {
    /** Checks one solution function against every example in the puzzle statement. */
    private fun checkSolution(
        solve: (String) -> Either<AocError, Long>,
        cases: List<Pair<String, Either<AocError, Long>>>,
    ) = cases.forEach { (input, expected) ->
        assertEquals(expected, solve(input), "failed on input $input")
    }

    private val partOneCases =
        listOf(
            "(())" to 0L,
            "()()" to 0L,
            "(((" to 3L,
            "(()(()(" to 3L,
            "))(((((" to 3L,
            "())" to -1L,
            "))(" to -1L,
            ")))" to -3L,
            ")())())" to -3L,
        )

    private val partTwoCases = listOf(")" to 1L, "()())" to 5L)

    @Test
    fun `part one solves the examples`() =
        checkSolution(::solvePartOne, partOneCases.map { (input, floor) -> input to floor.right() })

    @Test
    fun `part two solves the examples`() =
        checkSolution(
            ::solvePartTwo,
            partTwoCases.map { (input, position) -> input to position.right() },
        )

    @Test
    fun `a trailing newline is ignored`() =
        checkSolution(::solvePartOne, listOf("(()\n" to 1L.right()))

    @Test
    fun `an unexpected character is an error`() =
        checkSolution(::solvePartOne, listOf("(x)" to AocError.UnexpectedCharacter('x', 2).left()))

    @Test
    fun `never entering the basement is an error`() =
        checkSolution(::solvePartTwo, listOf("(()" to AocError.NeverEntersBasement.left()))
}
