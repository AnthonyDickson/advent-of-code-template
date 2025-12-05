# Name as cli to avoid name collision with "aoc" directory
BINARY = cli

.PHONY: test run build benchmark lint fmt clean

test:
	go test ./aoc/...

run:
	go run ./cmd/aoc

$(BINARY):
	go build -o $(BINARY) ./cmd/aoc

benchmark: $(BINARY)
	hyperfine -N ./$(BINARY)

fmt:
	go fmt ./...

lint:
	golangci-lint run

clean:
	rm -f $(BINARY)
