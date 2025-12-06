import Testing

@testable import AoC

@Test(
  "Part One Examples",
  arguments: [
    ("", 0),
    ("example1", 42),
    ("example2", 123),
    ("example3", 456),
  ]) func testPartOne(input: String, expected: Int)
{
  let actual = solvePartOne(input)

  #expect(expected == actual)
}

@Test(
  "Part Two Examples",
  arguments: [
    ("", 0),
    ("example1", 42),
    ("example2", 123),
    ("example3", 456),
  ]) func testPartTwo(input: String, expected: Int)
{
  let actual = solvePartTwo(input)

  #expect(expected == actual)
}
