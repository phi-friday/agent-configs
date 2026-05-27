#!/usr/bin/env bash
# Find which command/test creates unwanted file or state.
# Copy and adapt TEST_COMMAND_FOR_FILE for the project's test runner.
# Usage: bash find-polluter.template.sh <pollution_path> <file1> [file2 ...]

set -euo pipefail

if [ "$#" -lt 2 ]; then
  printf 'Usage: %s <pollution_path> <file1> [file2 ...]\n' "$0" >&2
  exit 2
fi

POLLUTION_PATH="$1"
shift

TEST_COMMAND_FOR_FILE() {
  local test_file="$1"
  # Replace with the project runner, for example:
  # npm test -- "$test_file"
  # pytest "$test_file"
  # cargo test --test "$test_file"
  printf 'TODO: edit TEST_COMMAND_FOR_FILE for %s\n' "$test_file" >&2
  return 2
}

for test_file in "$@"; do
  rm -rf "$POLLUTION_PATH"

  printf '\n=== Running %s ===\n' "$test_file"
  TEST_COMMAND_FOR_FILE "$test_file"

  if [ -e "$POLLUTION_PATH" ]; then
    printf '\nPOLLUTER=%s\n' "$test_file"
    printf 'CREATED=%s\n' "$POLLUTION_PATH"
    exit 1
  fi
done

printf '\nNo polluter found.\n'
