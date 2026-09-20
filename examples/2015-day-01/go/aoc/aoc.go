package aoc

import "fmt"

func SolvePartOne(input string) int {
	floor := 0

	for _, char := range input {
		floor += step(char)
	}

	return floor
}

func SolvePartTwo(input string) int {
	floor := 0

	for i, char := range input {
		floor += step(char)

		if floor == -1 {
			return 1 + i
		}
	}

	return 0
}

func step(char rune) int {
	switch char {
	case '(':
		return 1
	case ')':
		return -1
	default:
		panic(fmt.Sprintf("unexpected character %q", char))
	}
}
