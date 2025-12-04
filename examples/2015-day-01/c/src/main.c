#define _POSIX_C_SOURCE 1
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#include "aoc.h"

#define MAX_FILE_SIZE (1024 * 1024) // 1 MiB

char *read_file(const char *filename, size_t *out_size) {
  FILE *file = fopen(filename, "r");
  if (!file) {
    perror("Error opening file");
    return NULL;
  }

  struct stat st;
  if (fstat(fileno(file), &st) == -1) {
    perror("Error getting file size");
    fclose(file);
    return NULL;
  }

  if (st.st_size == 0) {
    fprintf(stderr, "Input file is empty\n");
    fclose(file);
    return NULL;
  }

  if (st.st_size > MAX_FILE_SIZE) {
    fprintf(stderr, "File too large (max %d bytes)\n", MAX_FILE_SIZE);
    fclose(file);
    return NULL;
  }

  char *buffer = malloc(st.st_size + 1);
  if (!buffer) {
    fprintf(stderr, "Memory allocation failed\n");
    fclose(file);
    return NULL;
  }

  size_t bytes_read = fread(buffer, 1, st.st_size, file);
  fclose(file);

  if (bytes_read != (size_t)st.st_size) {
    fprintf(stderr, "Error reading file: expected %ld bytes, got %zu\n",
            st.st_size, bytes_read);
    free(buffer);
    return NULL;
  }

  buffer[bytes_read] = '\0';
  if (out_size) {
    *out_size = bytes_read;
  }

  return buffer;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
    return EXIT_FAILURE;
  }

  size_t input_size;
  char *input = read_file(argv[1], &input_size);
  if (!input) {
    return EXIT_FAILURE;
  }

  printf("%d\n", solve_part_one(input));
  printf("%d\n", solve_part_two(input));

  free(input);
  return EXIT_SUCCESS;
}
