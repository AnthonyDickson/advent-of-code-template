SRC = src/aoc.gleam

.PHONY: test run build benchmark clean

test:
	gleam test

run:
	gleam run

build: $(SRC)
	gleam export erlang-shipment

benchmark: build
	hyperfine --warmup 3 -N "./build/erlang-shipment/entrypoint.sh run"

clean:
	rm -f build
