/**
 * `(` goes up one floor, `)` goes down one, and anything else leaves the floor alone.
 *
 * @param char A single instruction.
 * @returns The floor change the instruction asks for.
 */
function floorDelta(char: string): number {
  switch (char) {
    case "(":
      return 1;
    case ")":
      return -1;
    default:
      return 0;
  }
}

/**
 * Solves part one of the puzzle for the given input.
 *
 * @param input The puzzle input.
 * @returns The floor Santa ends up on.
 */
export function solvePartOne(input: string): number {
  let floor = 0;
  for (const char of input) {
    floor += floorDelta(char);
  }
  return floor;
}

/**
 * Solves part two of the puzzle for the given input.
 *
 * @param input The puzzle input.
 * @returns The position of the first instruction that takes him to the basement.
 */
export function solvePartTwo(input: string): number {
  let floor = 0;
  for (const [index, char] of [...input].entries()) {
    floor += floorDelta(char);
    if (floor === -1) {
      return index + 1;
    }
  }
  return 0;
}
