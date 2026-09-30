#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

printf '\n[Charlie] Starting frontend static server...\n'
cd "$FRONTEND_DIR"
python -m http.server 8080 >/tmp/charlie_frontend.log 2>&1 &
SERVER_PID=$!

sleep 2

printf '\n[Charlie] Frontend server PID: %s\n' "$SERVER_PID"
printf '[Charlie] Browser check target: http://localhost:8080\n'
printf '[Charlie] Benchmark checklist: page load, wake-action, transcript, speech flow, console errors\n'

kill "$SERVER_PID"
printf '\n[Charlie] Frontend verification script complete.\n'
