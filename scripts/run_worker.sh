#!/usr/bin/env bash
# MVP: scheduler runs inside the API process — use run_api.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Worker is embedded in the API process for this MVP."
echo "Start the API instead:"
echo "  ./scripts/run_api.sh"
echo ""
echo "The APScheduler runs mock ingestion every 30 minutes alongside FastAPI."
