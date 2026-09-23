open Alcotest

let test_part_one expected input =
  fun () -> check int "solves part one" expected (Aoc.solve_part_one input)
;;

let test_part_two expected input =
  fun () -> check int "solves part two" expected (Aoc.solve_part_two input)
;;

let () =
  run
    "AoC"
    [ "Part One", [ test_case "Example 1" `Quick (test_part_one 0 "") ]
    ; "Part Two", [ test_case "Example 1" `Quick (test_part_two 0 "") ]
    ]
;;
