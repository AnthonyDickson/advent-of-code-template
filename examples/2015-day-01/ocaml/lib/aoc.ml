let step floor instruction =
  match instruction with
  | '(' -> floor + 1
  | ')' -> floor - 1
  | _ -> floor
;;

let solve_part_one input_text = String.fold_left step 0 input_text

let solve_part_two input_text =
  input_text
  |> String.to_seq
  |> Seq.scan step 0
  |> Seq.drop 1
  |> Seq.find_index (fun floor -> floor = -1)
  |> Option.fold ~none:0 ~some:(fun index -> index + 1)
;;
