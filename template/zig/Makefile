SRC := $(wildcard src/*.zig)
EXE = ./zig-out/bin/aoc

.PHONY: test run benchmark fmt clean

test:
	zig build --watch test

run:
	zig build run

fmt:
	zig fmt src/

$(EXE): $(SRC)
	zig build --release=fast

benchmark: $(EXE)
	hyperfine --warmup 3 -N $(EXE)
	time -v $(EXE)

clean:
	rm -rf zig-out/
