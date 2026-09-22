-- The entry point: it reads `input.txt` and prints both answers, one per line.
-- Run it with `just run`, which pipes this script into the DuckDB CLI.
--
-- `.read` is a DuckDB CLI command, not SQL, which is why this file is run
-- through the CLI rather than named on the command line.

.read src/aoc.sql

SELECT solve_part_one(content) FROM read_text('input.txt');
SELECT solve_part_two(content) FROM read_text('input.txt');
