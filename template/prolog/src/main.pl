:- use_module(library(readutil), [read_file_to_string/3]).
:- use_module(aoc).

%% main is det.
%
%  Reads `input.txt` and prints both solutions, one per line.
main :-
    read_file_to_string('input.txt', Input, []),
    solve_part_one(Input, PartOne),
    solve_part_two(Input, PartTwo),
    format("~w~n~w~n", [PartOne, PartTwo]).
