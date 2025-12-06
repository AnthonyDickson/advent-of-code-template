CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g
SRC_DIR = src
TEST_DIR = tests

# Source files
AOC_SOURCES = $(SRC_DIR)/aoc.c
MAIN_SOURCE = $(SRC_DIR)/main.c
HEADERS = $(SRC_DIR)/aoc.h

# Object files
AOC_OBJ = $(SRC_DIR)/aoc.o

# Targets
MAIN = aoc
TEST = test_aoc

.PHONY: all clean test run

all: $(MAIN)

# Build main program (links main.c with aoc.o)
$(MAIN): $(MAIN_SOURCE) $(AOC_OBJ) $(HEADERS)
	$(CC) $(CFLAGS) -o $(MAIN) $(MAIN_SOURCE) $(AOC_OBJ)

# Compile aoc.c to object file
$(AOC_OBJ): $(AOC_SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -c $(AOC_SOURCES) -o $(AOC_OBJ)

# Build and run tests (link with aoc object file)
test: $(TEST)
	./$(TEST)

$(TEST): $(TEST_DIR)/test_aoc.c $(AOC_OBJ) $(HEADERS)
	$(CC) $(CFLAGS) -o $(TEST) $(TEST_DIR)/test_aoc.c $(AOC_OBJ)

# Run the solution
run: $(MAIN)
	./$(MAIN) input.txt

clean:
	rm -f $(MAIN) $(TEST) $(SRC_DIR)/*.o

benchmark:
	$(CC) $(CFLAGS) -O3 -o $(MAIN) $(MAIN_SOURCE) $(AOC_OBJ)
	hyperfine --warmup 3 -N "./$(MAIN) input.txt"
