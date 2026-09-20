from pathlib import Path

type Floor = int
type Index = int


def step(char: str) -> int:
    match char:
        case "(":
            return 1
        case ")":
            return -1
        case other:
            raise ValueError(f"Unexpected char: {other}")


def solve_part_one(data: str) -> Floor:
    floor = 0

    for char in data:
        floor += step(char)

    return floor


def solve_part_two(data: str) -> Index:
    floor = 0

    for index, char in enumerate(data, start=1):
        floor += step(char)

        if floor == -1:
            return index

    return 0


def main() -> None:
    data = Path("input.txt").read_text(encoding="utf-8")

    print(solve_part_one(data))
    print(solve_part_two(data))


if __name__ == "__main__":
    main()
