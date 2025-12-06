.PHONY: test run build benchmark fmt clean

test:
	zig build --watch test

run:
	zig build --watch run

build:
	zig build --release=fast

fmt:
	zig fmt src/

benchmark: build
	hyperfine -N ./zig-out/bin/aoc

clean:
	rm -rf zig-out/
