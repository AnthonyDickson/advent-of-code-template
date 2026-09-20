import random

import pytest

from aoc_lottery.lottery import Lottery


def test_chances_add_up_to_one():
    lottery = Lottery({"python": 3, "rust": 1})
    assert sum(entry.chance for entry in lottery.entries) == pytest.approx(1.0)
    assert lottery.entries[0].language == "python"
    assert lottery.entries[0].percent == pytest.approx(75.0)


def test_zero_weight_languages_leave_the_wheel():
    lottery = Lottery({"python": 1, "rust": 0})
    assert [entry.language for entry in lottery.entries] == ["python"]


def test_empty_wheel_is_rejected():
    with pytest.raises(ValueError, match="above zero"):
        Lottery({"python": 0, "rust": 0})


def test_draw_respects_weights():
    lottery = Lottery({"python": 4, "rust": 1}, rng=random.Random(20261225))
    drawn = [lottery.draw().language for _ in range(4000)]
    assert drawn.count("python") > drawn.count("rust") * 2


def test_draw_can_be_seeded():
    first = Lottery({"python": 1, "rust": 1}, rng=random.Random(7))
    second = Lottery({"python": 1, "rust": 1}, rng=random.Random(7))
    assert [first.draw().language for _ in range(5)] == [second.draw().language for _ in range(5)]


def test_draw_only_returns_known_languages():
    lottery = Lottery({"python": 2, "rust": 1, "zig": 1}, rng=random.Random(1))
    assert {lottery.draw().language for _ in range(50)} <= {"python", "rust", "zig"}


def test_rows_can_be_looked_up():
    lottery = Lottery({"python": 1, "rust": 1})
    assert lottery.row_of("rust") == 1
    with pytest.raises(KeyError):
        lottery.row_of("cobol")
