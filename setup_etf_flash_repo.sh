#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./setup_etf_flash_repo.sh etf_flash_repo.zip [target_dir]
#
# Example:
#   ./setup_etf_flash_repo.sh etf_flash_repo.zip etf-flash-crash-2015
#
# If target_dir is omitted, it defaults to etf-flash-crash-2015

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <zip-file> [target-dir]"
  exit 1
fi

ZIP_FILE="$1"
TARGET_DIR="${2:-etf-flash-crash-2015}"

if [ ! -f "$ZIP_FILE" ]; then
  echo "Error: ZIP file '$ZIP_FILE' not found."
  exit 1
fi

echo "Creating target directory: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

echo "Unzipping $ZIP_FILE into $TARGET_DIR ..."
unzip -q "$ZIP_FILE" -d "$TARGET_DIR"

cd "$TARGET_DIR"

# Optional: initialize Git repo
if [ ! -d ".git" ]; then
  echo "Initializing git repository..."
  git init >/dev/null
  git add .
  git commit -m "Initial import of ETF flash crash teaching repo skeleton" >/dev/null || true
fi

echo "Repository ready in: $(pwd)"
echo "You can now open this folder in your editor or connect Claude Code / Codex here."
