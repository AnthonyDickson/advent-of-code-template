open Alcotest

let test_part_one () = check int "solves part one" 0 (Aoc.solve_part_one "")
let test_part_two () = check int "solves part two" 0 (Aoc.solve_part_two "")

let () =
  run "AoC"
    [
      ("Part One", [ test_case "Example 1" `Quick test_part_one ]);
      ("Part Two", [ test_case "Example 1" `Quick test_part_two ]);
    ]
