Aoc :: {}.{
	solve_part_one : Str -> I64
	solve_part_one = |input| {
		input.to_utf8().fold(0, move)
	}

	solve_part_two : Str -> I64
	solve_part_two = |input| {
		walk = input
			.to_utf8()
			.fold_until(
				{ floor: 0, position: 0, basement: 0 },
				|state, byte| {
					floor = move(state.floor, byte)
					position = state.position + 1

					if floor == -1 {
						Break({ floor, position, basement: position })
					} else {
						Continue({ floor, position, basement: state.basement })
					}
				},
			)

		walk.basement
	}

	move : I64, U8 -> I64
	move = |floor, byte| match byte {
		'(' => floor + 1
		')' => floor - 1
		_ => floor
	}

	expect solve_part_one("(())") == 0
	expect solve_part_one("())") == -1
	expect solve_part_two(")") == 1
	expect solve_part_two("()())") == 5
}
