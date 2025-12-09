EXE = ./zig-out/bin/aoc

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
	hyperfine --warmup 3 -N $(EXE)
	time -v $(EXE)

clean:
	rm -rf zig-out/
