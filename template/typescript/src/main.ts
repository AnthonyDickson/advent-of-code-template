import { solvePartOne, solvePartTwo } from "./aoc.ts";

if (import.meta.main) {
  const input = Deno.readTextFileSync("input.txt");

  console.log(solvePartOne(input));
  console.log(solvePartTwo(input));
}
