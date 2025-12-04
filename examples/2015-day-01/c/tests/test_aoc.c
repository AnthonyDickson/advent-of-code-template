#include <stdio.h>
#include <stdlib.h>

#include "../src/aoc.h"

struct TestCase {
  const char *input;
  int expected;
};

static int tests_run = 0;
static int tests_failed = 0;

#define TEST(name) void name()

#define ASSERT_EQ(actual, expected, input)                                     \
  do {                                                                         \
    if (actual != expected) {                                                  \
      printf("FAIL: %s:%d - Test Case #%zu failed on input \"%s\". Expected "  \
             "%d, got %d\n",                                                   \
             __FILE__, __LINE__, i, input, expected, actual);                  \
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
  const struct TestCase cases[] = {
      {"(())", 0}, {"()()", 0}, {"(((", 3},  {"(()(()(", 3},  {"))(((((", 3},
      {"())", -1}, {"))(", -1}, {")))", -3}, {")())())", -3},
  };

  size_t num_cases = sizeof(cases) / sizeof(cases[0]);

  for (size_t i = 0; i < num_cases; ++i) {
    const char *input = cases[i].input;
    int expected = cases[i].expected;

    const int actual = solve_part_one(input);

    ASSERT_EQ(actual, expected, input);
  }
}

TEST(test_part_two) {
  const struct TestCase cases[] = {
      {")", 1},
      {"()())", 5},
  };

  size_t num_cases = sizeof(cases) / sizeof(cases[0]);

  for (size_t i = 0; i < num_cases; ++i) {
    const char *input = cases[i].input;
    int expected = cases[i].expected;

    const int actual = solve_part_two(input);

    ASSERT_EQ(actual, expected, input);
  }
}

int main() {
  printf("Running tests...\n");

  RUN_TEST(test_part_one);
  RUN_TEST(test_part_two);

  print_test_summary();
  return (tests_failed > 0) ? EXIT_FAILURE : EXIT_SUCCESS;
}
