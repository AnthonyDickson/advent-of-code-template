import pytest

from aoc import solve_part_one, solve_part_two

part_one_examples = [
    ("(())", 0),
    ("()()", 0),
    ("(((", 3),
    ("(()(()(", 3),
    ("))(((((", 3),
    ("())", -1),
    ("))(", -1),
    (")))", -3),
    (")())())", -3),
]
part_two_examples = [
    (")", 1),
    ("()())", 5),
]


@pytest.mark.parametrize(("puzzle_input", "expected"), part_one_examples)
def test_part_one(puzzle_input: str, expected: int) -> None:
    assert solve_part_one(puzzle_input) == expected


@pytest.mark.parametrize(("puzzle_input", "expected"), part_two_examples)
def test_part_two(puzzle_input: str, expected: int) -> None:
    assert solve_part_two(puzzle_input) == expected
