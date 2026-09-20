import pytest

from main import solve

solutions = [
    (")", -1, 1),
    ("()())", -1, 5),
    ("(())", 0, 0),
    ("()()", 0, 0),
    ("(((", 3, 0),
    ("(()(()(", 3, 0),
    ("))(((((", 3, 1),
    ("())", -1, 3),
    ("))(", -1, 1),
    (")))", -3, 1),
    (")())())", -3, 1),
]


@pytest.mark.parametrize(("data", "expected_floor", "expected_index"), solutions)
def test_solve(data: str, expected_floor: int, expected_index: int) -> None:
    actual_floor, actual_index = solve(data)

    assert actual_floor == expected_floor
    assert actual_index == expected_index
