Aoc :: {}.{
	solve_part_one : Str -> I64
	solve_part_one = |input| {
		input.to_utf8().fold(
			0,
			|floor, byte| {
				if byte == '(' {
					floor + 1
				} else {
					floor - 1
				}
			},
		)
	}

	solve_part_two : Str -> I64
	solve_part_two = |input| {
		walk = input
			.to_utf8()
			.fold_until(
				{ floor: 0, position: 0 },
				|state, byte| {
					floor = if byte == '(' {
						state.floor + 1
					} else {
						state.floor - 1
					}
					next = { floor, position: state.position + 1 }

					if floor == -1 {
						Break(next)
					} else {
						Continue(next)
					}
				},
			)

		walk.position
	}

	expect solve_part_one("(())") == 0
	expect solve_part_one("())") == -1
	expect solve_part_two(")") == 1
	expect solve_part_two("()())") == 5
}
