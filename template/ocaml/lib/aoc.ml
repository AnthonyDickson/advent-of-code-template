let load_input filename =
  let ic = In_channel.open_text filename in
  let content = In_channel.input_lines ic in
  In_channel.close ic;
  content

let solve_part_one _s =
  0

let solve_part_two _s =
  0
