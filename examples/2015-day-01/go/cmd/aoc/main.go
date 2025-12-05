package main

import (
	"fmt"
	"os"

	"github.com/anthonydickson/advent-of-code-template/aoc"
)

func main() {
	contents, err := os.ReadFile("input.txt")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading input file: %v\n", err)
		os.Exit(1)
	}

	input := string(contents)
	fmt.Println(aoc.SolvePartOne((input)))
	fmt.Println(aoc.SolvePartTwo((input)))
}
