package aoc_test

import (
	"testing"

	"github.com/anthonydickson/advent-of-code-template/aoc"
)

func TestPartOne(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  int
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
			got := aoc.SolvePartOne(tt.input)

			if got != tt.want {
				t.Errorf("SolvePartOne(%q) = %d, want %d", tt.input, got, tt.want)
			}
		})
	}
}

func TestPartTwo(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  int
	}{
		{"example 1", ")", 1},
		{"example 2", "()())", 5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := aoc.SolvePartTwo(tt.input)

			if got != tt.want {
				t.Errorf("SolvePartTwo(%q) = %d, want %d", tt.input, got, tt.want)
			}
		})
	}
}
