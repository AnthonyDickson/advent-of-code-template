-- Day 1: Not Quite Lisp.
--
-- `(` goes up one floor, `)` goes down one, and anything else leaves the floor
-- where it is.

-- The instructions of `input`, one row each, paired with their 1-based position.
CREATE OR REPLACE MACRO instructions(input) AS TABLE
    SELECT instruction, position
    FROM unnest(regexp_extract_all(input, '.')) WITH ORDINALITY AS t(instruction, position);

-- Moves one floor for a single instruction.
CREATE OR REPLACE MACRO move(instruction) AS
    CASE
        WHEN instruction = '(' THEN 1
        WHEN instruction = ')' THEN -1
        ELSE 0
    END;

-- Solves part one: the floor Santa is on once every instruction is done.
CREATE OR REPLACE MACRO solve_part_one(input) AS (
    SELECT coalesce(sum(move(instruction)), 0) FROM instructions(input)
);

-- Solves part two: the position of the instruction that first takes Santa below
-- the ground floor.
CREATE OR REPLACE MACRO solve_part_two(input) AS (
    SELECT coalesce(min(position), 0)
    FROM (
        SELECT position, sum(move(instruction)) OVER (ORDER BY position) AS floor
        FROM instructions(input)
    )
    WHERE floor < 0
);
