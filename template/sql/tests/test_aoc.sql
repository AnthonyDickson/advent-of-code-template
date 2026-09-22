-- The examples from the puzzle statement, one list per part. `just test` runs
-- this script, which checks every case and prints a summary, so a run that
-- reaches its summary is a run where every example passed.
--
-- `assert_example` aborts the run on the first case that fails, naming the input
-- it was given.

.read src/aoc.sql

CREATE OR REPLACE MACRO assert_example(label, actual, expected) AS
    CASE
        WHEN actual IS NOT DISTINCT FROM expected THEN true
        ELSE error('FAIL ' || label || ': expected ' || expected || ', got ' || actual)
    END;

WITH part_one AS (
    SELECT assert_example('part one on ' || input, solve_part_one(input), expected) AS passed
    FROM (VALUES
        ('', 0)
    ) AS examples(input, expected)
),
part_two AS (
    SELECT assert_example('part two on ' || input, solve_part_two(input), expected) AS passed
    FROM (VALUES
        ('', 0)
    ) AS examples(input, expected)
)
SELECT 'all ' || count(*) || ' examples passed'
FROM (SELECT * FROM part_one UNION ALL SELECT * FROM part_two);
