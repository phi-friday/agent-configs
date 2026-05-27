#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps, and run it when a manual action is unavoidable.
# The script structures the human step and prints captured answers for the agent.

set -euo pipefail

step() {
  local instruction="$1"
  printf '\nSTEP: %s\n' "$instruction"
  printf 'Press Enter when done. '
  read -r _
}

capture() {
  local name="$1"
  local question="$2"
  local value
  printf '\n%s\n' "$question"
  printf '> '
  read -r value
  printf -v "$name" '%s' "$value"
}

# --- edit below ---------------------------------------------------------

step "Open the app or system state that reproduces the issue."

capture REPRODUCED "Did the reported failure reproduce? (yes/no)"
capture SYMPTOM "Paste the exact error, wrong output, or visible symptom."
capture NOTES "Any timing, account, environment, browser, or data details?"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'REPRODUCED=%s\n' "$REPRODUCED"
printf 'SYMPTOM=%s\n' "$SYMPTOM"
printf 'NOTES=%s\n' "$NOTES"
