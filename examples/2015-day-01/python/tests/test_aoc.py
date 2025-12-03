import unittest
from unittest import TestCase

from main import solve


class TestAoc(TestCase):
    def test(self):
        cases = (
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
        )

        for input, expected_floor, expected_index in cases:
            actual_floor, actual_index = solve(input)

            self.assertEqual(expected_floor, actual_floor, f"wrong floor for input {input}")
            self.assertEqual(expected_index, actual_index, f"wrong index for input {input}")


if __name__ == "__main__":
    unittest.main()
