package aoc

import kotlin.test.Test
import kotlin.test.assertEquals

class AocTest {
    /** Checks one solution function against every example in the puzzle statement. */
    private fun checkSolution(
        solve: (String) -> Long,
        cases: List<Pair<String, Long>>,
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

    @Test fun `part one solves the examples`() = checkSolution(::solvePartOne, partOneCases)

    @Test fun `part two solves the examples`() = checkSolution(::solvePartTwo, partTwoCases)

    @Test
    fun `never entering the basement gives zero`() =
        checkSolution(::solvePartTwo, listOf("(()" to 0L))

    @Test
    fun `a trailing newline is ignored`() = checkSolution(::solvePartOne, listOf("(()\n" to 1L))
}
