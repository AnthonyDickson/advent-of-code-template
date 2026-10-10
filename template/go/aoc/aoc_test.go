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
		{"example 1", "test input", 0},
		{"example 2", "other input", 0},
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
		{"example 1", "test input", 0},
		{"example 2", "other input", 0},
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
