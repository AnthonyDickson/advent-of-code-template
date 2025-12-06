.PHONY: build run test benchmark fmt clean

build:
	dune build

run:
	dune exec aoc -w

test:
	dune runtest -w

fmt:
	dune build @fmt --auto-promote

benchmark: build
	hyperfine --warmup 3 -N ./_build/default/bin/main.exe

clean:
	dune clean
