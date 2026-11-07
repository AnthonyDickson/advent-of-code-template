package aoc

import kotlin.test.Test
import kotlin.test.assertEquals

class AocTest {
    /** Checks one solution function against the example in the puzzle statement. */
    private fun checkSolution(solve: (String) -> Long, input: String, expected: Long) =
        assertEquals(expected, solve(input), "failed on input $input")

    @Test fun `part one solves the example`() = checkSolution(::solvePartOne, "", 0)

    @Test fun `part two solves the example`() = checkSolution(::solvePartTwo, "", 0)
}
