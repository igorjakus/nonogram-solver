(* Builds a hint specification matching the given row
   Example: [0, 1, 1, 0, 0, 1, 1, 1, 1] -> [2, 4] *)
let build_hint row = 
  let rec help r acc streak = 
    match r with
    | [] -> if streak > 0 then List.rev (streak::acc) else List.rev acc
    | true :: r -> help r acc (streak+1)
    | false :: r ->
      match streak with
      | 0 -> help r acc 0 
      | _ -> help r (streak :: acc) 0
  in help row [] 0;;

let verify_row hint row = (build_hint row) = hint;;

let verify_rows hints rows = List.for_all2 verify_row hints rows;;

let rec transpose = function
  | [] | [] :: _ -> []
  | list -> (List.map List.hd list) :: transpose (List.map List.tl list);; 

let ( let* ) xs f = List.concat_map f xs;;

let rec cartesian_product = function 
  | [] -> [[]]
  | xs :: xss -> let* xs = xs in let* yss = cartesian_product xss in [xs :: yss];;

(* Generates all rows of length n composed of false and true *)
let gen_rows n = cartesian_product (List.init n (fun _ -> [true; false]))

let build_row hint length = List.filter (fun row -> verify_row hint row) (gen_rows length)

let build_candidate (hints : int list list) (length : int) =
  let possible_rows = List.map (fun hint -> build_row hint length) hints
  in cartesian_product possible_rows;;

type nonogram_spec = { rows : int list list ; cols : int list list }

let solve_nonogram nono =
  build_candidate (nono.rows) (List.length (nono.cols))
  |> List.filter (fun xss -> transpose xss |> verify_rows nono.cols);;
