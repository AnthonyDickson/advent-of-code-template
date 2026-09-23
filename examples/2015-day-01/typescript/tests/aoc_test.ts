import { assertEquals } from "@std/assert";

import { solvePartOne, solvePartTwo } from "../src/aoc.ts";

const partOneCases: [string, number][] = [
  ["(())", 0],
  ["()()", 0],
  ["(((", 3],
  ["(()(()(", 3],
  ["))(((((", 3],
  ["())", -1],
  ["))(", -1],
  [")))", -3],
  [")())())", -3],
];

const partTwoCases: [string, number][] = [
  [")", 1],
  ["()())", 5],
];

Deno.test("part one solves the examples", () => {
  for (const [input, expected] of partOneCases) {
    assertEquals(solvePartOne(input), expected, `failed on input ${JSON.stringify(input)}`);
  }
});

Deno.test("part two solves the examples", () => {
  for (const [input, expected] of partTwoCases) {
    assertEquals(solvePartTwo(input), expected, `failed on input ${JSON.stringify(input)}`);
  }
});
