let load_input filename = In_channel.with_open_text filename In_channel.input_lines
let explode_string str = List.of_seq (String.to_seq str)

let solve_part_one lines =
  let rec aux floor chars =
    match chars with
    | [] -> floor
    | h :: t -> if Char.equal h '(' then aux (floor + 1) t else aux (floor - 1) t
  in
  let chars = explode_string (String.concat "" lines) in
  aux 0 chars
;;

let solve_part_two lines =
  let rec aux index floor chars =
    match chars with
    | [] -> index
    | h :: t ->
      if Char.equal h '('
      then aux (index + 1) (floor + 1) t
      else if floor > 0
      then aux (index + 1) (floor - 1) t
      else index
  in
  let chars = explode_string (String.concat "" lines) in
  aux 1 0 chars
;;
