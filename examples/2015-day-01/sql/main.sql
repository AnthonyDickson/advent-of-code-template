-- The entry point: it reads `input.txt` and prints both answers, one per line.
-- Run it with `just run`, which hands this script to the DuckDB CLI with `-f`.
--
-- `.read` is a DuckDB CLI command, not SQL, which is why this file is run by
-- the CLI as a script rather than sent to DuckDB as a query.

.read src/aoc.sql

SELECT solve_part_one(content) FROM read_text('input.txt');
SELECT solve_part_two(content) FROM read_text('input.txt');
