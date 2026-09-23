let load_input filename = In_channel.with_open_text filename In_channel.input_all

let () =
  let problem_input = load_input "input.txt" in
  print_int (Aoc.solve_part_one problem_input);
  print_newline ();
  print_int (Aoc.solve_part_two problem_input);
  print_newline ()
;;
