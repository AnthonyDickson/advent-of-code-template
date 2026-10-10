:- use_module('../src/aoc.pl').

:- begin_tests(aoc).

test(part_one_solves_the_placeholder, Actual =:= 0) :-
    solve_part_one("", Actual).

test(part_two_solves_the_placeholder, Actual =:= 0) :-
    solve_part_two("", Actual).

:- end_tests(aoc).
