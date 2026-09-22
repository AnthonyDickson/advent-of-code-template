package aoc

floor_delta :: proc(c: rune) -> int {
	switch c {
	case '(':
		return 1
	case ')':
		return -1
	}
	return 0
}

solve_part_one :: proc(input: string) -> int {
	floor := 0

	for c in input {
		floor += floor_delta(c)
	}

	return floor
}

solve_part_two :: proc(input: string) -> int {
	floor := 0

	for c, i in input {
		floor += floor_delta(c)

		if floor == -1 {
			return i + 1
		}
	}

	return 0
}
