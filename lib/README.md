# Shared libraries

Helpers that are useful across many Advent of Code days, kept out of `template/` and `examples/` so those stay small and
each helper has a single home.

Each language gets its own folder, `lib/<lang>/`, containing a complete, self-contained project: source, tests, a
`justfile`, and a `README.md`, exactly like a template but with no puzzle to solve. The folder is the reference
implementation when the same helper is ported to another language, and it is built and tested in that language's dev
shell.

```shell
nix develop .#fsharp -c sh -c 'cd lib/fsharp && just test'
```

- [`fsharp/`](./fsharp/README.md) - a small parser combinator library for parsing puzzle input.
