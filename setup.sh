#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
LINK_PATH="$HOME/.agents"

echo "[INFO] script dir: $SCRIPT_DIR"
echo "[INFO] link path : $LINK_PATH"

echo "[INFO] creating symlink..."
ln -s "$SCRIPT_DIR" "$LINK_PATH"

echo "[INFO] done"
echo "[INFO] $LINK_PATH -> $SCRIPT_DIR"
