import pytest

from main import solve_part_one, solve_part_two

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


@pytest.mark.parametrize(("data", "expected"), part_one_examples)
def test_part_one(data: str, expected: int) -> None:
    assert solve_part_one(data) == expected


@pytest.mark.parametrize(("data", "expected"), part_two_examples)
def test_part_two(data: str, expected: int) -> None:
    assert solve_part_two(data) == expected
