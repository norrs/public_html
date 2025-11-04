#!/usr/bin/env bash
set -euo pipefail

python scripts/watch_history.py &
WATCH_PID=$!

cleanup() {
  if ps -p "$WATCH_PID" >/dev/null 2>&1; then
    kill "$WATCH_PID" 2>/dev/null || true
  fi
  wait "$WATCH_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

hugo server -D --disableFastRender --bind 0.0.0.0 --port 1313
