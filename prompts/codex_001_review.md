# Codex Prompt 001 - Watchtower Scaffold Review

ROLE CHECK: Codex
PROFILE CHECK: P5 Review/Debug
MISSION SLICE: Review the first Watchtower scaffold for architecture, safety, and VultureInv integration correctness.

## Read First

- `AGENTS.md`
- `README.md`
- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/mission.md`
- `DOC/architecture.md`
- `DOC/data_sources.md`
- `DOC/telegram_bot_spec.md`
- `DOC/specs/vultureinv_support_plan.md`
- `DOC/specs/settings_and_web_integration.md`
- `DOC/vultureinv_integration_contract.md`
- `prompts/claude_001_scaffold.md`
- changed implementation files

## Review Focus

- Provider calls are isolated behind adapters.
- Route handlers stay thin.
- Mock ingestion proves the full loop.
- Telegram commands are access-controlled.
- Secrets are not committed.
- Snapshot metadata includes source and freshness state.
- VultureInv integration does not bypass the main cockpit's responsibility.
- No automated trading or out-of-scope assets were introduced.

## Expected Output

Findings first, ordered by severity, with file/line references.

If safe, provide a concise next implementation prompt for:

1. FRED provider,
2. OpenDART provider,
3. KRX/pykrx provider,
4. SEC EDGAR provider.
