class AocSuite extends munit.FunSuite:
  /** Checks one solution function against the example in the puzzle statement. */
  private def checkSolution(solve: String => Long, input: String, expected: Long): Unit =
    assertEquals(solve(input), expected, s"failed on input $input")

  test("part one solves the example"):
    checkSolution(solvePartOne, "", 0L)

  test("part two solves the example"):
    checkSolution(solvePartTwo, "", 0L)
