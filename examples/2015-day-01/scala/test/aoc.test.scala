class AocSuite extends munit.FunSuite:
  /** Checks one solution function against every example in the puzzle statement. */
  private def checkSolution(solve: String => Long, cases: Seq[(String, Long)]): Unit =
    for (input, expected) <- cases do
      assertEquals(solve(input), expected, s"failed on input $input")

  private val partOneCases = Seq(
    "(())" -> 0L,
    "()()" -> 0L,
    "(((" -> 3L,
    "(()(()(" -> 3L,
    "))(((((" -> 3L,
    "())" -> -1L,
    "))(" -> -1L,
    ")))" -> -3L,
    ")())())" -> -3L
  )

  private val partTwoCases = Seq(")" -> 1L, "()())" -> 5L)

  test("part one solves the examples"):
    checkSolution(solvePartOne, partOneCases)

  test("part two solves the examples"):
    checkSolution(solvePartTwo, partTwoCases)
