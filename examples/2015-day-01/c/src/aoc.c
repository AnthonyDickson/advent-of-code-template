#include "aoc.h"

int solve_part_one(const char *input) {
  int floor = 0;
  int i = 0;

  while (input[i] != '\0') {
    switch (input[i]) {
      case '(':
        floor += 1;
        break;
      case ')':
        floor -= 1;
        break;
    }
    
    i++;
  }
  
  return floor;
}

int solve_part_two(const char *input) {
  int floor = 0;
  int i = 0;

  while (input[i] != '\0') {
    switch (input[i]) {
      case '(':
        floor += 1;
        break;
      case ')':
        floor -= 1;
        break;
    }
    
    i++;

    if (floor == -1) {
      return i;
    }
  }
  
  return i;
}
