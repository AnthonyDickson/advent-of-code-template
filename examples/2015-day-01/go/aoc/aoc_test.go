package aoc_test

import (
	"testing"

	"github.com/anthonydickson/advent-of-code-template/aoc"
)

func TestPartOne(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"example 1", "(())", 0},
		{"example 2", "()()", 0},
		{"example 3", "(((", 3},
		{"example 4", "(()(()(", 3},
		{"example 5", "))(((((", 3},
		{"example 6", "())", -1},
		{"example 7", "))(", -1},
		{"example 8", ")))", -3},
		{"example 9", ")())())", -3},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := aoc.SolvePartOne(tt.input)

			if actual != tt.expected {
				t.Errorf("failed for %s %q: expected %d, got %d", tt.name, tt.input, tt.expected, actual)
			}
		})
	}
}

func TestPartTwo(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"example 1", ")", 1},
		{"example 2", "()())", 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := aoc.SolvePartTwo(tt.input)

			if actual != tt.expected {
				t.Errorf("failed for %s %q: expected %d, got %d", tt.name, tt.input, tt.expected, actual)
			}
		})
	}
}
