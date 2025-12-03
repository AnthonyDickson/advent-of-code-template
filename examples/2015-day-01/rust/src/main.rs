use std::fs;

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();

    let part_one_solution = solve_part_one(&input);
    let part_two_solution = solve_part_two(&input);

    println!("{part_one_solution}");
    println!("{part_two_solution}");
}

fn solve_part_one(input: &str) -> i64 {
    let mut floor = 0;

    for char in input.chars() {
        match char {
            '(' => floor += 1,
            ')' => floor -= 1,
            other => panic!("got unexpected char '{other}'"),
        }
    }

    return floor;
}

fn solve_part_two(input: &str) -> usize {
    let mut floor = 0;

    for (i, char) in input.chars().enumerate() {
        match char {
            '(' => floor += 1,
            ')' => floor -= 1,
            other => panic!("got unexpected char '{other}'"),
        }

        if floor == -1 {
            return 1 + i;
        }
    }

    return 0;
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
