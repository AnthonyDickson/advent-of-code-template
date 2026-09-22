package main

import "core:fmt"
import "core:os"

import aoc "aoc"

main :: proc() {
	data, err := os.read_entire_file("input.txt", context.allocator)
	if err != nil {
		fmt.eprintln("could not read input.txt:", err)
		os.exit(1)
	}
	defer delete(data)

	input := string(data)
	fmt.println(aoc.solve_part_one(input))
	fmt.println(aoc.solve_part_two(input))
}
