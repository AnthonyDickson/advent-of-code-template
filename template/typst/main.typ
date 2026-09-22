// The entry point. It reads `input.txt` once, shows both answers when it is
// rendered, and exposes them as `<part-one>` and `<part-two>` metadata, which
// is how `just run` gets the answers out of a document.

#import "/src/aoc.typ": solve-part-one, solve-part-two

#let input = read("input.txt")
#let part-one = solve-part-one(input)
#let part-two = solve-part-two(input)

= Advent of Code

#table(
  columns: 2,
  [Part one], [#part-one],
  [Part two], [#part-two],
)

#metadata(part-one) <part-one>
#metadata(part-two) <part-two>
