from pathlib import Path

Floor = int
Index = int


def solve(data: str) -> tuple[Floor, Index]:
    floor = 0
    index = 0

    for i, char in enumerate(data):
        match char:
            case "(":
                floor += 1
            case ")":
                floor -= 1
            case other:
                raise RuntimeError(f"Unexpected char: {other}")

        if index == 0 and floor == -1:
            index = 1 + i

    return floor, index


def main() -> None:
    data = Path("input.txt").read_text(encoding="utf-8")

    part_one_solution, part_two_solution = solve(data)

    print(part_one_solution)
    print(part_two_solution)


if __name__ == "__main__":
    main()
