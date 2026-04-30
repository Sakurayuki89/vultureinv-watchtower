#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
    source .venv/bin/activate
fi

exec uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
