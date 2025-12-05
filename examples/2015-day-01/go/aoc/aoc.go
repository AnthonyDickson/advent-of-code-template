package aoc

func SolvePartOne(input string) int {
	floor := 0

	for _, char := range input {
		switch char {
		case '(':
			floor += 1
		case ')':
			floor -= 1
		}
	}

	return floor
}

func SolvePartTwo(input string) int {
	floor := 0

	for i, char := range input {
		switch char {
		case '(':
			floor += 1
		case ')':
			floor -= 1
		}

		if floor == -1 {
			return 1 + i
		}
	}

	return 0
}
