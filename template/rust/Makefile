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
	hyperfine -N ./target/release/aoc

clean:
	cargo clean

