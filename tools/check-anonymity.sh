#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TERM_FILE="$ROOT_DIR/tools/anonymity_terms.txt"
TARGETS=("$ROOT_DIR/index.html" "$ROOT_DIR/static")
status=0

if ! command -v rg >/dev/null 2>&1; then
  echo "error: ripgrep (rg) is required for the anonymity check." >&2
  exit 2
fi

echo "Checking deployed site files for common anonymity leaks..."

patterns=(
  '[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}'
  '/Users/[A-Za-z0-9._-]+'
  '/home/[A-Za-z0-9._-]+'
  'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+'
  'overleaf\.com/project/[A-Za-z0-9]+'
)

for pattern in "${patterns[@]}"; do
  if rg -n --pcre2 "$pattern" "${TARGETS[@]}"; then
    echo "leak pattern matched: $pattern" >&2
    status=1
  fi
done

if [[ -f "$TERM_FILE" ]]; then
  while IFS= read -r term; do
    [[ -z "$term" || "$term" =~ ^[[:space:]]*# ]] && continue
    if rg -n -i -F -- "$term" "${TARGETS[@]}"; then
      echo "sensitive term matched: $term" >&2
      status=1
    fi
  done < "$TERM_FILE"
fi

if [[ "$status" -eq 0 ]]; then
  echo "No configured anonymity leaks found in deployable site files."
else
  echo "Anonymity check failed. Remove the matches above before review release." >&2
fi

PYTHON_BIN="python3"
CODEX_PYTHON="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [[ -x "$CODEX_PYTHON" ]]; then
  PYTHON_BIN="$CODEX_PYTHON"
fi

if command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  if ! "$PYTHON_BIN" "$ROOT_DIR/tools/check-pdfs.py"; then
    status=1
  fi
else
  echo "warning: python3 not found; skipped PDF checks." >&2
fi

exit "$status"
