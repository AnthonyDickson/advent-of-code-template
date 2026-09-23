:- module(aoc, [solve_part_one/2, solve_part_two/2]).
:- use_module(library(apply), [maplist/3]).
:- use_module(library(lists), [sum_list/2]).

%% floor_step(+Char, -Delta) is det.
%
%  `(` goes up one floor, `)` goes down one, and anything else leaves the
%  floor alone.
floor_step('(', 1).
floor_step(')', -1).
floor_step(_, 0).

%% solve_part_one(+Input, -Result) is det.
%
%  Solves part one of the puzzle. `Input` is the whole puzzle input as a
%  string; unify `Result` with the answer.
solve_part_one(Input, Result) :-
    string_chars(Input, Chars),
    maplist(floor_step, Chars, Deltas),
    sum_list(Deltas, Result).

%% solve_part_two(+Input, -Result) is det.
%
%  Solves part two of the puzzle. `Input` is the whole puzzle input as a
%  string; unify `Result` with the answer.
solve_part_two(Input, Result) :-
    string_chars(Input, Chars),
    first_basement(Chars, 1, 0, Result).

%% first_basement(+Chars, +Position, +Floor, -Result) is det.
%
%  The 1-based position of the first character that takes the floor below
%  zero, or 0 if it never happens.
first_basement([Char|Rest], Position, Floor, Result) :-
    floor_step(Char, Delta),
    NextFloor is Floor + Delta,
    (   NextFloor < 0
    ->  Result = Position
    ;   NextPosition is Position + 1,
        first_basement(Rest, NextPosition, NextFloor, Result)
    ).
first_basement([], _, _, 0).
