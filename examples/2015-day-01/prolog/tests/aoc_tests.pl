:- use_module('../src/aoc.pl').

:- begin_tests(aoc).

test(part_one_solves_the_examples,
     [forall(member(case(Input, Expected),
                    [ case("(())", 0),
                      case("()()", 0),
                      case("(((", 3),
                      case("(()(()(", 3),
                      case("))(((((", 3),
                      case("())", -1),
                      case("))(", -1),
                      case(")))", -3),
                      case(")())())", -3)
                    ]))]) :-
    solve_part_one(Input, Expected).

test(part_two_solves_the_examples,
     [forall(member(case(Input, Expected), [case(")", 1), case("()())", 5)]))]) :-
    solve_part_two(Input, Expected).

:- end_tests(aoc).
