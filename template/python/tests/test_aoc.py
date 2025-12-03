import unittest
from unittest import TestCase

from main import solve_part_one, solve_part_two


class TestAoc(TestCase):
    def test_part_one(self):
        input = ""
        expected = 0

        actual = solve_part_one(input)

        self.assertEqual(expected, actual, f"failed for input {input}")

    def test_part_two(self):
        input = ""
        expected = 0

        actual = solve_part_two(input)

        self.assertEqual(expected, actual, f"failed for input {input}")


if __name__ == "__main__":
    unittest.main()
