open Alcotest

let test_part_one expected s =
 fun () -> check int "solves part one" expected (Aoc.solve_part_one s)

let test_part_two expected s =
 fun () -> check int "solves part two" expected (Aoc.solve_part_two s)

let () =
  run "AoC"
    [
      ( "Part One",
        [
          test_case "Example 1" `Quick (test_part_one 0 "(())");
          test_case "Example 2" `Quick (test_part_one 0 "()()");
          test_case "Example 3" `Quick (test_part_one 3 "(((");
          test_case "Example 4" `Quick (test_part_one 3 "(()(()(");
          test_case "Example 5" `Quick (test_part_one 3 "))(((((");
          test_case "Example 6" `Quick (test_part_one (-1) "())");
          test_case "Example 7" `Quick (test_part_one (-1) "))(");
          test_case "Example 8" `Quick (test_part_one (-3) ")))");
          test_case "Example 8" `Quick (test_part_one (-3) ")())())");
        ] );
      ( "Part Two",
        [
          test_case "Example 1" `Quick (test_part_two 1 ")");
          test_case "Example 2" `Quick (test_part_two 5 "()())");
        ] );
    ]
