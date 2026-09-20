from pathlib import Path


def solve_part_one(data: str) -> int:
    return 0


def solve_part_two(data: str) -> int:
    return 0


def main() -> None:
    data = Path("input.txt").read_text(encoding="utf-8")

    print(solve_part_one(data))
    print(solve_part_two(data))


if __name__ == "__main__":
    main()
