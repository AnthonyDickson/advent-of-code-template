#include <stdio.h>
#include <stdlib.h>

#include "../src/aoc.h"

static int tests_run = 0;
static int tests_failed = 0;

#define TEST(name) void name()

#define ASSERT_EQ(actual, expected)                                            \
  do {                                                                         \
    if ((actual) != (expected)) {                                              \
      printf("FAIL: %s:%d - Expected %d, got %d\n", __FILE__, __LINE__,        \
             (expected), (actual));                                            \
      tests_failed++;                                                          \
      return;                                                                  \
    }                                                                          \
  } while (0)

#define RUN_TEST(test)                                                         \
  do {                                                                         \
    int initial_failures = tests_failed;                                       \
    printf("Running %s...", #test);                                            \
    tests_run++;                                                               \
    test();                                                                    \
    if (initial_failures == tests_failed) {                                    \
      printf(" PASS\n");                                                       \
    }                                                                          \
  } while (0)

void print_test_summary() {
  printf("\n--- Test Summary ---\n");
  printf("Tests Run: %d\n", tests_run);

  if (tests_failed > 0) {
    printf("Tests Failed: %d\n", tests_failed);
    printf("Result: FAILURE!\n");
  } else {
    printf("Result: SUCCESS! All tests passed.\n");
  }
}

TEST(test_part_one) {
  const char *input = "";
  const int expected = 0;

  const int actual = solve_part_one(input);

  ASSERT_EQ(actual, expected);
}

TEST(test_part_two) {
  const char *input = "";
  const int expected = 0;

  const int actual = solve_part_two(input);

  ASSERT_EQ(actual, expected);
}

int main() {
  printf("Running tests...\n");

  RUN_TEST(test_part_one);
  RUN_TEST(test_part_two);

  print_test_summary();
  return (tests_failed > 0) ? EXIT_FAILURE : EXIT_SUCCESS;
}
