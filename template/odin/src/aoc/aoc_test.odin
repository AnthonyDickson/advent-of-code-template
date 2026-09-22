#+test
package aoc

import "core:testing"

@(test)
test_part_one :: proc(t: ^testing.T) {
	input := ""
	expected := 0

	actual := solve_part_one(input)

	testing.expect_value(t, actual, expected)
}

@(test)
test_part_two :: proc(t: ^testing.T) {
	input := ""
	expected := 0

	actual := solve_part_two(input)

	testing.expect_value(t, actual, expected)
}
