#+test
package aoc

import "core:testing"

@(test)
test_part_one :: proc(t: ^testing.T) {
	cases := [?]struct {
		input:    string,
		expected: int,
	} {
		{input = "(())", expected = 0},
		{input = "()()", expected = 0},
		{input = "(((", expected = 3},
		{input = "(()(()(", expected = 3},
		{input = "))(((((", expected = 3},
		{input = "())", expected = -1},
		{input = "))(", expected = -1},
		{input = ")))", expected = -3},
		{input = ")())())", expected = -3},
	}

	for c in cases {
		actual := solve_part_one(c.input)
		testing.expectf(
			t,
			actual == c.expected,
			"%s: expected %d, got %d",
			c.input,
			c.expected,
			actual,
		)
	}
}

@(test)
test_part_two :: proc(t: ^testing.T) {
	cases := [?]struct {
		input:    string,
		expected: int,
	}{{input = ")", expected = 1}, {input = "()())", expected = 5}}

	for c in cases {
		actual := solve_part_two(c.input)
		testing.expectf(
			t,
			actual == c.expected,
			"%s: expected %d, got %d",
			c.input,
			c.expected,
			actual,
		)
	}
}
