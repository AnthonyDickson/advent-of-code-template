let load_input filename = In_channel.with_open_text filename In_channel.input_all
let explode_string str = List.init (String.length str) (String.get str)

let solve_part_one str =
  let rec aux floor chars =
    match chars with
    | [] -> floor
    | h :: t -> if h = '(' then aux (floor + 1) t else aux (floor - 1) t
  in
  let chars = explode_string str in
  aux 0 chars
;;

let solve_part_two str =
  let rec aux index floor chars =
    match chars with
    | [] -> index
    | h :: t ->
      if h = '('
      then aux (index + 1) (floor + 1) t
      else if floor > 0
      then aux (index + 1) (floor - 1) t
      else index
  in
  let chars = explode_string str in
  aux 1 0 chars
;;
