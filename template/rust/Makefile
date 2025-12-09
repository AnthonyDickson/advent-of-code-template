EXE = ./target/release/aoc

.PHONY: test run build benchmark fmt clean

test:
	cargo test

run:
	cargo run

fmt:
	cargo fmt

build:
	cargo build --release

benchmark: build
	hyperfine --warmup 3 -N $(EXE) 
	time -v $(EXE)

clean:
	cargo clean

