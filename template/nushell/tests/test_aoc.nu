# The examples from the puzzle statement, one table per part. `just test` runs
# this script, which asserts every case and prints a summary, so a run that
# reaches its summary is a run where every example passed.

use std/assert
use ../src/aoc.nu [solve-part-one, solve-part-two]

let part_one_examples = [
    [input, expected];
    ['', 0]
]

let part_two_examples = [
    [input, expected];
    ['', 0]
]

for case in $part_one_examples {
    assert equal (solve-part-one $case.input) $case.expected $"part one on ($case.input | to nuon)"
}

for case in $part_two_examples {
    assert equal (solve-part-two $case.input) $case.expected $"part two on ($case.input | to nuon)"
}

let checked = ($part_one_examples | length) + ($part_two_examples | length)
print $"all ($checked) examples passed"
