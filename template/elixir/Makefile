MAIN = lib/aoc.ex lib/aoc/cli.ex

.PHONY: test run build benchmark fmt clean

test:
	mix test

build: $(MAIN)
	mix escript.build

run: build
	./aoc

benchmark: build
	hyperfine --warmup 3 -N ./aoc

fmt:
	mix format

clean:
	mix clean

