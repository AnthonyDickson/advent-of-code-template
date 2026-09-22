# The two solutions. `main.nu` hands them the puzzle input, and the tests in
# `tests/test_aoc.nu` hand them the examples from the puzzle statement.

# Solves part one: the floor Santa is standing on once every instruction is done.
export def solve-part-one [input: string]: nothing -> int {
    $input
    | str trim
    | split chars
    | each { |char| if $char == "(" { 1 } else { -1 } }
    | math sum
}

# Solves part two: the position of the instruction that first takes Santa below
# the ground floor.
export def solve-part-two [input: string]: nothing -> int {
    mut floor = 0
    mut position = 0
    for char in ($input | str trim | split chars) {
        $position += 1
        $floor += (if $char == "(" { 1 } else { -1 })
        if $floor < 0 {
            return $position
        }
    }
    0
}
