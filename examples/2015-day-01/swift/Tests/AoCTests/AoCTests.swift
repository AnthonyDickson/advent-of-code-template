import Testing

@testable import AoC

@Test(
  "Part One Examples",
  arguments: [
    (")", -1),
    ("()())", -1),
    ("(())", 0),
    ("()()", 0),
    ("(((", 3),
    ("(()(()(", 3),
    ("))(((((", 3),
    ("())", -1),
    ("))(", -1),
    (")))", -3),
    (")())())", -3),
  ]) func testPartOne(input: String, expected: Int)
{
  let actual = solvePartOne(input)

  #expect(expected == actual)
}

@Test(
  "Part Two Examples",
  arguments: [
    (")", 1),
    ("()())", 5),
  ]) func testPartTwo(input: String, expected: Int)
{
  let actual = solvePartTwo(input)

  #expect(expected == actual)
}
