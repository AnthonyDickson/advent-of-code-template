.PHONY: test run benchmark clean

test:
	gleam test

run:
	gleam run

benchmark:
	gleam export erlang-shipment
	hyperfine -N "./build/erlang-shipment/entrypoint.sh run"

clean:
	rm -f build
