SRC := $(wildcard src/*.gleam)
BIN = ./build/erlang-shipment/entrypoint.sh

.PHONY: test run build benchmark clean

test:
	gleam test

run:
	gleam run

$(BIN): $(SRC)
	gleam export erlang-shipment

benchmark: $(BIN)
	hyperfine --warmup 3 -N "$(BIN) run"
	time -v ./build/erlang-shipment/entrypoint.sh run

clean:
	rm -f build
