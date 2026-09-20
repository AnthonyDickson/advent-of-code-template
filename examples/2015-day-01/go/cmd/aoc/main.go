package main

import (
	"fmt"
	"log"
	"os"

	"github.com/anthonydickson/advent-of-code-template/aoc"
)

func main() {
	contents, err := os.ReadFile("input.txt")
	if err != nil {
		log.Fatalf("Error reading input file: %v", err)
	}

	input := string(contents)
	fmt.Println(aoc.SolvePartOne(input))
	fmt.Println(aoc.SolvePartTwo(input))
}
