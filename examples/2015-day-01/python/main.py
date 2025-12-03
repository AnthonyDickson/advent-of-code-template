def main():
    with open("input.txt", "r") as f:
        input = f.read()

    part_one_solution, part_two_solution = solve(input)
    print(part_one_solution)
    print(part_two_solution)


Floor = int
Index = int


def solve(input: str) -> tuple[Floor, Index]:
    floor = 0
    index = 0

    for i, char in enumerate(input):
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


if __name__ == "__main__":
    main()
