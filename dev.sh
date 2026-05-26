#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

if [ ! -d "$ROOT_DIR/backend/.venv" ]; then
  echo "Missing backend/.venv. Run backend setup from README first."
  exit 1
fi

if [ ! -d "$ROOT_DIR/frontend/node_modules" ]; then
  echo "Missing frontend/node_modules. Run frontend setup from README first."
  exit 1
fi

echo "Starting backend on http://localhost:8000"
(
  cd "$ROOT_DIR/backend"
  source .venv/bin/activate
  uvicorn app.main:app --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!

echo "Starting frontend on http://localhost:5173"
(
  cd "$ROOT_DIR/frontend"
  bun run dev --host 0.0.0.0
) &
FRONTEND_PID=$!

echo
echo "Open http://localhost:5173"
echo "Press Ctrl-C to stop both servers."
echo

while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
  sleep 1
done
