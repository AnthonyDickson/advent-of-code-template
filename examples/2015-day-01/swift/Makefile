SRC_DIR = Sources/
TEST_DIR  = Tests/
BUILD_DIR = .build/
SRC = Sources/AoCCLI/main.swift
MAIN_PKG  = aoc-cli

.PHONY: test run build benchmark fmt clean

test:
	swift test --disable-xctest

run:
	swift run $(MAIN_PKG)

fmt:
	swift format --in-place --recursive $(SRC_DIR) $(TEST_DIR)

build: $(SRC)
	swift build -c release

benchmark: build
	hyperfine --warmup 3 -N .build/release/AoC

clean:
	rm -rf $(BUILD_DIR)

