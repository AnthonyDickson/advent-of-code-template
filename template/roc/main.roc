app [main!] {
	cli: platform "https://github.com/roc-lang/basic-cli/releases/download/0.22.2/9zUBxb1LtXYVc4eR4hAtd1WQDwBYDhM6HQdZz1UFCm2m.tar.zst",
	roc: "nightly-2026-09-19-d025939",
}

import cli.OsStr
import cli.Path
import cli.Stdout
import src/Aoc

main! = |_args| {
	input = Path.read_utf8!(Path.from_os_str(OsStr.from_str("input.txt")))?

	Stdout.line!(Aoc.solve_part_one(input).to_str())?
	Stdout.line!(Aoc.solve_part_two(input).to_str())
}
