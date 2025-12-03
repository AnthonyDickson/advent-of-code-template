use std::fs;

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();

    let part_one_solution = solve_part_one(&input);
    let part_two_solution = solve_part_two(&input);

    println!("{part_one_solution}");
    println!("{part_two_solution}");
}

fn solve_part_one(_input: &str) -> i64 {
    return 0;
}

fn solve_part_two(_input: &str) -> i64 {
    return 0;
}

#[cfg(test)]
mod tests {
    use crate::{solve_part_one, solve_part_two};

    #[test]
    fn solves_part_one() {
        let input = "";
        let expected = 0;

        let actual = solve_part_one(input);

        assert_eq!(actual, expected, "failed on input \"{input}\"")
    }

    #[test]
    fn solves_part_two() {
        let input = "";
        let expected = 0;

        let actual = solve_part_two(input);

        assert_eq!(actual, expected, "failed on input \"{input}\"")
    }
}
