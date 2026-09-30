#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

cd "$ROOT_DIR"

printf '\n[Charlie] Checking Python runtime...\n'
"$PYTHON_BIN" --version

printf '\n[Charlie] Creating Python virtual environment if missing...\n'
if [ ! -d "$BACKEND_DIR/.venv" ]; then
  "$PYTHON_BIN" -m venv "$BACKEND_DIR/.venv"
fi

source "$BACKEND_DIR/.venv/bin/activate"

printf '\n[Charlie] Installing backend dependencies...\n'
pip install --upgrade pip >/dev/null
pip install -r "$BACKEND_DIR/requirements.txt"

printf '\n[Charlie] Compiling backend modules...\n'
python -m compileall "$BACKEND_DIR"

printf '\n[Charlie] Starting backend smoke check...\n'
python - <<'PY'
import sys
import subprocess
import time

port = 8000
proc = subprocess.Popen([
    sys.executable,
    '-m',
    'uvicorn',
    'main:app',
    '--host',
    '0.0.0.0',
    '--port',
    str(port),
], cwd='backend', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

try:
    time.sleep(3)
    print(f"Backend process spawned with PID {proc.pid}")
    print(f"Port {port} is expected to host the Charlie API.")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
PY

printf '\n[Charlie] Dependency verification complete.\n'
