#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Watchtower validation"
echo "Root: $ROOT"
echo

required_files=(
  "AGENTS.md"
  "README.md"
  ".env.example"
  "DOC/mission.md"
  "DOC/architecture.md"
  "DOC/data_sources.md"
  "DOC/telegram_bot_spec.md"
  "DOC/mac_mini_runbook.md"
  "DOC/vultureinv_integration_contract.md"
  "DOC/collaboration/ai_role_protocol.md"
  "DOC/collaboration/context_tool_profiles.md"
  "DOC/specs/vultureinv_support_plan.md"
  "DOC/specs/settings_and_web_integration.md"
  "prompts/claude_001_scaffold.md"
  "prompts/codex_001_review.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "[FAIL] missing $file"
    exit 1
  fi
  echo "[PASS] $file exists"
done

if grep -RInE "(api[_-]?key|token|secret|password) *= *['\"][^'\"]{8,}" \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=venv \
  --exclude-dir=__pycache__ \
  --exclude-dir=data \
  --exclude=.env.example \
  .; then
  echo "[FAIL] possible committed secret"
  exit 1
fi
echo "[PASS] secret pattern scan passed"

if [[ -d app ]]; then
  python3 -m py_compile $(find app -name '*.py')
  echo "[PASS] python compile scan completed"
else
  echo "[SKIP] app/ not created yet"
fi

echo
echo "Validation passed."
