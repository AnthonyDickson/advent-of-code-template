# Name as cli to avoid name collision with "aoc" directory
BINARY = cli
SRC = aoc/aoc.go

.PHONY: test run build benchmark lint fmt clean

test:
	go test ./aoc/...

run:
	go run ./cmd/aoc

$(BINARY): $(SRC)
	go build -o $(BINARY) ./cmd/aoc

benchmark: $(BINARY)
	hyperfine --time-unit microsecond --warmup 3 -N ./$(BINARY)
	time -v ./$(BINARY)

fmt:
	go fmt ./...

lint:
	golangci-lint run

clean:
	rm -f $(BINARY)
