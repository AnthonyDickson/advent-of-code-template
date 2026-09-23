use std::fs;

fn main() {
    let input = fs::read_to_string("input.txt").expect("failed to read input.txt");

    let part_one_solution = solve_part_one(&input);
    let part_two_solution = solve_part_two(&input);

    println!("{part_one_solution}");
    println!("{part_two_solution}");
}

fn step(floor: i64, instruction: char) -> i64 {
    match instruction {
        '(' => floor + 1,
        ')' => floor - 1,
        _ => floor,
    }
}

fn solve_part_one(input: &str) -> i64 {
    input.chars().fold(0, step)
}

fn solve_part_two(input: &str) -> i64 {
    let mut floor = 0;

    for (index, instruction) in input.chars().enumerate() {
        floor = step(floor, instruction);

        if floor == -1 {
            return index as i64 + 1;
        }
    }

    0
}

#[cfg(test)]
mod tests {
    use crate::{solve_part_one, solve_part_two};

    #[test]
    fn solves_part_one() {
        let cases = [
            ("(())", 0),
            ("()()", 0),
            ("(((", 3),
            ("(()(()(", 3),
            ("))(((((", 3),
            ("())", -1),
            ("))(", -1),
            (")))", -3),
            (")())())", -3),
        ];

        for (input, expected) in cases {
            let actual = solve_part_one(input);

            assert_eq!(actual, expected, "failed on input \"{input}\"")
        }
    }

    #[test]
    fn solves_part_two() {
        let cases = [(")", 1), ("()())", 5)];

        for (input, expected) in cases {
            let actual = solve_part_two(input);

            assert_eq!(actual, expected, "failed on input \"{input}\"")
        }
    }
}
