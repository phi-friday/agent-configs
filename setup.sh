#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
LINK_PATH="$HOME/.agents"
INSTALLER="$SCRIPT_DIR/install_locked_skills.py"

echo "[INFO] script dir: $SCRIPT_DIR"
echo "[INFO] link path : $LINK_PATH"

if [[ -e "$LINK_PATH" || -L "$LINK_PATH" ]]; then
	if [[ -d "$LINK_PATH" && "$(cd -- "$LINK_PATH" && pwd -P)" == "$SCRIPT_DIR" ]]; then
		echo "[INFO] link path already points to this repo"
	else
		echo "[ERROR] link path already exists: $LINK_PATH" >&2
		exit 1
	fi
else
	echo "[INFO] creating symlink..."
	ln -s "$SCRIPT_DIR" "$LINK_PATH"
fi

echo "[INFO] installing lock-managed skills..."
uv run --script "$INSTALLER"

echo "[INFO] done"
echo "[INFO] $LINK_PATH -> $SCRIPT_DIR"
