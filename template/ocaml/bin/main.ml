let () =
  let problem_input = Aoc.load_input "input.txt" in
  print_int (Aoc.solve_part_one problem_input);
  print_newline ();
  print_int (Aoc.solve_part_two problem_input);
  print_newline ()
