// The examples from the puzzle statement, one case per row. `just test` calls
// `run-tests`, which panics on the first case that fails, so a run that prints
// its summary is a run where every example passed.

#import "/src/aoc.typ": solve-part-one, solve-part-two

#let part-one-examples = (
  ("(())", 0),
  ("()()", 0),
  ("(((", 3),
  ("(()(()(", 3),
  ("))(((((", 3),
  ("())", -1),
  ("))(", -1),
  (")))", -3),
  (")())())", -3),
)

#let part-two-examples = ((")", 1), ("()())", 5))

/// Checks both solutions against every example and returns a summary of the run.
#let run-tests() = {
  let checked = 0
  for (input, expected) in part-one-examples {
    assert.eq(
      solve-part-one(input),
      expected,
      message: "part one on " + repr(input),
    )
    checked += 1
  }
  for (input, expected) in part-two-examples {
    assert.eq(
      solve-part-two(input),
      expected,
      message: "part two on " + repr(input),
    )
    checked += 1
  }
  "all " + str(checked) + " examples passed"
}
